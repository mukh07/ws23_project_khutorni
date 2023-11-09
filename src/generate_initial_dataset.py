import argparse
import json
import os
import zipfile


from mmpose.apis import MMPoseInferencer


coco_keypoints = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle"
]


mpii_keypoints = [
    "right_ankle",
    "right_knee",
    "right_hip",
    "left_hip",
    "left_knee",
    "left_ankle",
    "pelvis",
    "thorax",
    "upper_neck",
    "head_top",
    "right_wrist",
    "right_elbow",
    "right_shoulder",
    "left_shoulder",
    "left_elbow",
    "left_wrist"
]


coco_to_mpii_index_mapping = {
    0: -1,
    1: -1,
    2: -1,
    3: -1,
    4: -1,
    5: 13,
    6: 12,
    7: 14,
    8: 11,
    9: 15,
    10: 10,
    11: 3,
    12: 2,
    13: 4,
    14: 1,
    15: 5,
    16: 0,
}


mpii_indices = range(16)
mpii_indices_mapped = coco_to_mpii_index_mapping.values()
mpii_indices_unmapped = [
    i for i in mpii_indices if i not in mpii_indices_mapped]
new_keypoints = [mpii_keypoints[i] for i in mpii_indices_unmapped]


extended_keypoints = coco_keypoints + new_keypoints
extended_skeleton = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 18], [18, 13],
    [6, 12], [7, 13], [7, 21], [21, 6], [6, 8], [7, 9], [8, 10],
    [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6],
    [5, 7], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23]
]


def generate_annotations(model, folder_path, out_dir):
    inferencer = MMPoseInferencer(pose2d=model)
    result_generator = inferencer(folder_path, pred_out_dir=out_dir)
    results = [result for result in result_generator]


def load_annotations(annotation_path):
    json_paths = os.listdir(annotation_path)
    annotations = {}
    num_annotations = 0
    for json_path in json_paths:
        img_id = int(json_path.split('.')[0])
        with open(os.path.join(annotation_path, json_path), 'r') as f:
            img_annos = json.load(f)
            annotations[img_id] = img_annos
            num_annotations += len(img_annos)

    return annotations, num_annotations


def remove_invalid_predictions(annotations, min_bbox_score=0.5, min_bbox_area=32,
                               min_keypoint_score=0.5, min_keypoints=3):
    """ Remove the 'invalid' predictions from the annotations.

    We define a prediction as invalid if either:
    1. The 'bbox_score' is less than a threshold.
    2. The 'bbox' area is less than a threshold.
    3. The number of keypoints with good scores is less than a threshold.
    """
    cleaned_annotations = {}
    for img_id, annotation in annotations.items():
        # annotation is a list of dictionaries, where each dictionary is
        # one detected person in the image, and has the following keys:
        # 'bbox', 'bbox_score', 'keypoints', 'keypoint_scores'
        cleaned_annotation = []
        for person in annotation:
            bboxes = person['bbox']  # list of [x, y, width, height]
            bbox_score = person['bbox_score']  # float
            keypoints = person['keypoints']  # list of [x, y] pairs
            keypoint_scores = person['keypoint_scores']  # list of floats

            # Filter out low-scoring bounding boxes.
            if bbox_score < min_bbox_score:
                continue

            # Filter out small bounding boxes.
            bbox_area = 0
            for bbox in bboxes:
                bbox_area += bbox[2] * bbox[3]
            if bbox_area < min_bbox_area * min_bbox_area:
                continue

            # Check if the keypoints are valid.
            num_valid_keypoints = sum(
                [score > min_keypoint_score for score in keypoint_scores])
            if num_valid_keypoints < min_keypoints:
                continue

            # If we get here, the prediction is valid.
            cleaned_annotation.append(person)

        cleaned_annotations[img_id] = cleaned_annotation

    return cleaned_annotations


def compute_iou(bbox1, bbox2):
    """Compute the Intersection over Union (IoU) of two bounding boxes.

    Args:
    bbox1, bbox2 -- the bounding boxes in format x, y, width, height.

    Returns:
    iou -- the IoU of bbox1 and bbox2.
    """

    # Determine the coordinates of the intersection rectangle
    x_left = max(bbox1[0], bbox2[0])
    y_top = max(bbox1[1], bbox2[1])
    x_right = min(bbox1[0] + bbox1[2], bbox2[0] + bbox2[2])
    y_bottom = min(bbox1[1] + bbox1[3], bbox2[1] + bbox2[3])

    # Compute the area of intersection rectangle
    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    # Compute the area of both the prediction and ground-truth rectangles
    bbox1_area = bbox1[2] * bbox1[3]
    bbox2_area = bbox2[2] * bbox2[3]

    # Compute the intersection over union by taking the intersection area and dividing it by the sum of prediction + ground-truth areas - the intersection area
    iou = intersection_area / \
        float(bbox1_area + bbox2_area - intersection_area)

    # return the intersection over union value
    return iou


def match_predictions(coco_preds, mpii_preds, min_bbox_overlap=0.75):
    # This function takes the predictions from the COCO and MPII models as input.
    # Each prediction includes keypoints, scores, and a bounding box.
    # The function returns a list of matches, where each match is a pair of predictions
    # (one from the COCO model and one from the MPII model) that have the highest IoU.

    matches = []

    # Compute the IoU for each pair of bounding boxes.
    for coco_pred in coco_preds:
        best_iou = 0
        best_match = None
        for mpii_pred in mpii_preds:
            iou = compute_iou(coco_pred['bbox'][0], mpii_pred['bbox'][0])
            if iou > best_iou:
                best_iou = iou
                best_match = mpii_pred

        # Add the match with the highest IoU to the list of matches.
        if best_match is not None and best_iou > min_bbox_overlap:
            matches.append((coco_pred, best_match))

    return matches


def merge_annotations(coco_annotations, mpii_annotations, min_bbox_overlap=0.75):
    global mpii_indices_unmapped
    global coco_to_mpii_index_mapping
    merged_annotations = {}
    for img_id, coco_annotation in coco_annotations.items():
        if img_id not in mpii_annotations:
            continue

        mpii_annotation = mpii_annotations[img_id]

        # Match the predictions from the COCO and MPII models.
        matches = match_predictions(coco_annotation, mpii_annotation, min_bbox_overlap)

        # Merge the predictions from the COCO and MPII models.
        merged_annotation = []
        for (coco_person, mpii_person) in matches:
            coco_person_kpts = coco_person['keypoints']
            coco_person_scores = coco_person['keypoint_scores']
            coco_person_bbox = coco_person['bbox'][0]
            coco_person_bbox_score = coco_person['bbox_score']

            mpii_person_kpts = mpii_person['keypoints']
            mpii_person_scores = mpii_person['keypoint_scores']
            mpii_person_bbox = mpii_person['bbox'][0]
            mpii_person_bbox_score = mpii_person['bbox_score']

            # Merge corresponding keypoints from the COCO and MPII models.
            extended_kpts = []
            extended_scores = []
            for coco_idx, mpii_idx in coco_to_mpii_index_mapping.items():
                coco_kpt = coco_person_kpts[coco_idx]
                coco_score = coco_person_scores[coco_idx]

                if mpii_idx == -1:
                    # This keypoint is not present in the MPII model.
                    # Use the keypoint from the COCO model.
                    extended_kpts.append(coco_kpt)
                    extended_scores.append(coco_score)
                    continue

                mpii_kpt = mpii_person_kpts[mpii_idx]
                mpii_score = mpii_person_scores[mpii_idx]

                merged_kpt = [0, 0]
                merged_score = 0

                if coco_score > mpii_score:
                    merged_kpt = coco_kpt
                    merged_score = coco_score
                else:
                    merged_kpt = mpii_kpt
                    merged_score = mpii_score

                extended_kpts.append(merged_kpt)
                extended_scores.append(merged_score)

            assert len(extended_kpts) == 17, len(extended_kpts)

            # Get the extra keypoints from the MPII model using `mpii_indices_unmapped`
            mpii_person_kpts_extra = [mpii_person_kpts[i]
                                      for i in mpii_indices_unmapped]
            mpii_person_kpts_scores_extra = [
                mpii_person_scores[i] for i in mpii_indices_unmapped]

            # Extend the COCO keypoints and scores with the extra keypoints from MPII.
            extended_kpts.extend(mpii_person_kpts_extra)
            extended_scores.extend(mpii_person_kpts_scores_extra)

            # Calculate two intermediate spine keypoints.
            pelvis = mpii_person_kpts_extra[0]
            pelvis_score = mpii_person_kpts_scores_extra[0]

            thorax = mpii_person_kpts_extra[1]
            thorax_score = mpii_person_kpts_scores_extra[1]

            spine_1_x = pelvis[0] + (thorax[0] - pelvis[0]) / 3
            spine_1_y = pelvis[1] + (thorax[1] - pelvis[1]) / 3
            spine_1_score = pelvis_score + (thorax_score - pelvis_score) / 3
            spine_1 = [spine_1_x, spine_1_y]

            spine_2_x = pelvis[0] + 2 * (thorax[0] - pelvis[0]) / 3
            spine_2_y = pelvis[1] + 2 * (thorax[1] - pelvis[1]) / 3
            spine_2_score = pelvis_score + 2 * \
                (thorax_score - pelvis_score) / 3
            spine_2 = [spine_2_x, spine_2_y]
            
            extended_kpts.extend([spine_1, spine_2])
            extended_scores.extend([spine_1_score, spine_2_score])

            assert len(extended_kpts) == 23, len(extended_kpts)
            assert len(extended_scores) == 23, len(extended_scores)

            # Merge the bounding boxes from the COCO and MPII models.
            merged_bbox = [0, 0, 0, 0]
            merged_bbox_score = 0
            if coco_person_bbox_score > mpii_person_bbox_score:
                merged_bbox = coco_person_bbox
                merged_bbox_score = coco_person_bbox_score

            else:
                merged_bbox = mpii_person_bbox
                merged_bbox_score = mpii_person_bbox_score

            # Add the merged annotation to the list of merged annotations.
            merged_annotation.append({
                'keypoints': extended_kpts,
                'keypoint_scores': extended_scores,
                'bbox': [merged_bbox],
                'bbox_score': merged_bbox_score
            })

        merged_annotations[img_id] = merged_annotation

    return merged_annotations


def convert_to_coco_json(annotations):
    # This function converts the merged annotations to the COCO format.
    # The COCO format is a list of dictionaries, where each dictionary
    # represents a single image. Each dictionary contains the image ID,
    # the image height and width, and the annotations for that image.
    # The annotations include the keypoints, the keypoint scores, the
    # bounding box, and the bounding box score.
    coco_style_annotations = []
    anno_id = 1
    for img_id, annotation in annotations.items():
        for person in annotation:
            kpts = person['keypoints']
            kpts_scores = person['keypoint_scores']
            bbox = person['bbox'][0]

            # Convert the keypoints from [x1, y1, x2, y2, ...] to [[x1, y1, v1], [x2, y2, v2], ...]
            kpts_with_visibility = []
            num_keypoints = 0
            for i, kpt in enumerate(kpts):
                kpt_x, kpt_y = kpt[0], kpt[1]
                kpt_score = kpts_scores[i]

                if kpt_x == 0 and kpt_y == 0:
                    visibility = 0
                elif kpt_score > 0.3:
                    num_keypoints += 1
                    visibility = 2
                else:
                    num_keypoints += 1
                    visibility = 1

                kpts_with_visibility.append(kpt_x)
                kpts_with_visibility.append(kpt_y)
                kpts_with_visibility.append(visibility)

            bbox_area = bbox[2] * bbox[3]
            coco_style_annotations.append({
                'image_id': img_id,
                'category_id': 1,
                'keypoints': kpts_with_visibility,
                'bbox': bbox,
                'num_keypoints': num_keypoints,
                'id': anno_id,
                "segmentation": [],
                "area": bbox_area,
                "iscrowd": 0,
            })

            anno_id += 1

    return coco_style_annotations


def main(args):
    coco_path = args.coco_path
    coco_split = args.coco_split
    folder_path = os.path.join(coco_path, coco_split)
    print('Processing images from:', folder_path)

    # Generate the COCO annotations.
    print('Predicting 17 keypoints using the COCO model...')
    coco_model = 'human'
    coco_annotations_path = f'./tmp/{coco_split}/coco'
    generate_annotations(coco_model, folder_path, coco_annotations_path)

    # Generate the MPII annotations.
    print('Predicting 16 keypoints using the MPII model...')
    mpii_model = 'rtmpose-m_8xb64-210e_mpii-256x256'
    mpii_annotations_path = f'./tmp/{coco_split}/mpii'
    generate_annotations(mpii_model, folder_path, mpii_annotations_path)

    # Load predicted annotations.
    coco_annotations, num_coco_predictions = load_annotations(
        coco_annotations_path)  # 17 keypoints (COCO)
    mpii_annotations, num_mpii_predictions = load_annotations(
        mpii_annotations_path)  # 16 keypoints (MPII)

    print('Number of annotations from COCO model:', num_coco_predictions)
    print('Number of annotations from MPII model:', num_mpii_predictions)

    # Remove invalid predictions.
    clean_kwargs = {
        'min_keypoints': args.min_keypoints,
        'min_keypoint_score': args.min_keypoint_score,
        'min_bbox_area': args.min_bbox_area,
        'min_bbox_score': args.min_bbox_score,
    }
    cleaned_coco_annotations = remove_invalid_predictions(
        coco_annotations, **clean_kwargs)
    cleaned_mpii_annotations = remove_invalid_predictions(
        mpii_annotations, **clean_kwargs)

    # Merge the annotations from the two models.
    merged_annotations = merge_annotations(
        cleaned_coco_annotations,
        cleaned_mpii_annotations,
        args.min_bbox_overlap,
    )

    # At this point, we have merged annotations in MMPose format, which we need to
    # convert to COCO format. The COCO format is a list of dictionaries, where each
    # dictionary represents a single detection.
    merged_annotation = convert_to_coco_json(merged_annotations)

    # Read the split info from the original COCO annotations.
    annotations_filename = f'person_keypoints_{coco_split}.json'
    split_annotations_path = os.path.join(coco_path, 'annotations',
                                          annotations_filename)
    with open(split_annotations_path, 'r') as f:
        original_coco_annotations = json.load(f)
    info = original_coco_annotations['info']
    licenses = original_coco_annotations['licenses']
    images = original_coco_annotations['images']
    print("Number of original COCO annotations:", len(original_coco_annotations['annotations']))

    # Create the extended COCO annotations dictionary.
    coco_extended = {
        "info": info,
        "licenses": licenses,
        "images": images,
        "annotations": merged_annotation,
        "categories": [{
            "supercategory": "person",
            "id": 1,
            "name": "person",
            "keypoints": [str(i) for i in range(1, 24)],
            "skeleton": [
                [16, 14], [14, 12], [17, 15], [15, 13], [12, 18], [18, 13],
                [6, 12], [7, 13], [7, 19], [19, 6], [6, 8], [7, 9], [8, 10],
                [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6],
                [5, 7], [18, 22], [22, 23], [23, 19], [19, 20], [20, 21]
            ]
        }]
    }

    # Save the extended COCO annotations.
    save_dir = args.save_path
    os.makedirs(save_dir, exist_ok=True)
    json_file = os.path.join(save_dir, annotations_filename)
    with open(json_file, 'w') as f:
        json.dump(coco_extended, f)

    # Archive the annotations in a ZIP file for loading into CVAT.
    archive_path = os.path.join(save_dir, f'{coco_split}.zip')
    with zipfile.ZipFile(archive_path, 'w') as zip_file:
        arcname = os.path.join('annotations', annotations_filename)
        zip_file.write(json_file, arcname=arcname)

    # Print the number of annotations
    print('Number of combined annotations:', len(merged_annotation))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--coco_path', default='data/coco')
    parser.add_argument('--coco_split', default='val2017')
    parser.add_argument('--save_path', default='data/coco-extended')
    # iou threshold for merging COCO and MPII detections
    parser.add_argument('--min_bbox_overlap', type=float, default=0.7)
    parser.add_argument('--min_bbox_score', type=float,
                        default=0.5)  # bbox above this are 'good'
    # min area of bbox in pixels
    parser.add_argument('--min_bbox_area', type=int, default=32)
    parser.add_argument('--min_keypoint_score', type=float,
                        default=0.3)  # kpts above this are 'good'
    # min number of 'good' kpts required to keep a person
    parser.add_argument('--min_keypoints', type=int, default=3)
    args = parser.parse_args()

    main(args)
