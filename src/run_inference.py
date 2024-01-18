import json
import os
# import zipfile
# from itertools import chain
from pathlib import Path
from pprint import pprint

from PIL import Image
from mmpose.apis import MMPoseInferencer
import torch
import torch.nn.functional as F
from datasets.datasets.body.coco_extended_dataset import CocoExtendedDataset

from generate_initial_dataset import get_cropped_image_path
from split_into_batches import zip_and_copy_images

SPLIT = "train"
MAIN_DIR = Path("data/coco-extended")
PIPELINE_DIR = MAIN_DIR / "al-pipeline"


def main():
    # read progress
    progress_path = PIPELINE_DIR / "progress.json"
    with open(progress_path) as f:
        progress = json.load(f)

    # determine which batch to run next
    # completed_dir = PIPELINE_DIR / SPLIT / "completed"
    # dirs = sorted(d.name for d in batches_dir.iterdir())
    batches_dir = MAIN_DIR / f'{SPLIT}2017'
    sorted_batches = sorted(d.name for d in batches_dir.iterdir())
    next_batch_name = progress[SPLIT]['next_batch_name']
    batches_completed = progress[SPLIT]['completed']

    if next_batch_name:
        next_batch_dir = batches_dir / next_batch_name
    elif not next_batch_name and batches_completed == 0:
        next_batch_dir = batches_dir / sorted_batches[0]
    elif not next_batch_name and batches_completed == len(sorted_batches):
        print("Nothing to do, all batches completed.")
        return

    # load annotations
    with open(next_batch_dir / "person_keypoints.json") as f:
        data = json.load(f)
        annotations = data['annotations']
        all_images = data['images']
        print("Loaded annotations.")

    # instantiate inferencer
    coco_extended_model = "configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py"
    inferencer = MMPoseInferencer(pose2d=coco_extended_model)
    print("Loaded inferencer.")

    image_dir = Path(f'data/coco/{SPLIT}2017')
    tmp_image_dir = Path(f'tmp/{SPLIT}2017')
    coco_extended_ann_path = Path(f'tmp/{SPLIT}2017/coco-extended')

    # for each annotation:
        # 1. crop image accordingly
        # 2. run inference on the cropped image
        # 3. take the 6 predicted values from model and confidence
        # 4. compute confidence by averagring confidence of the 6 scores
        # 5. mark those with score >= 0.5 as completed, those below as manual_labeling required

    markings = dict(
        completed=dict(images=[], annotations=[]),
        need_manual_labeling=dict(images=[], annotations=[])
    )

    for i, ann in enumerate(annotations):
        if (i + 1) % 100 == 0:
            print(f'Completed {i + 1} / {len(annotations)} images.')
        image_id, cropped_image_path = get_cropped_image_path(tmp_image_dir, ann)
        bbox = ann['bbox']
        x, y, width, height = bbox

        if width <= 0 or height <= 0:
            continue

        # crop Image
        image_path = image_dir / f'{image_id:012d}.jpg'
        img = Image.open(image_path)
        cropped = img.crop((x, y, x + width, y + height))
        cropped.save(cropped_image_path)

        # Generate annotation
        result_generator = inferencer([cropped_image_path], pred_out_dir=coco_extended_ann_path)
        predicted_ann = next(result_generator)
        predictions = predicted_ann['predictions'][0][0]

        # TODO: Testing
        # print("PREDICTIONS", predictions)
        print("KPT SCORES:")
        pprint(predictions['keypoint_scores'])
        # confidence_values = F.softmax(torch.tensor(predictions['keypoint_scores']), dim=0)
        # print("SOFTMAX values", confidence_values)
        # confidence_values = torch.sigmoid(torch.tensor(predictions['keypoint_scores']))
        # print("SIGMOID VALUES", confidence_values)
        os.remove(cropped_image_path)
        return


        keypoints = predictions['keypoints'][-6:]
        keypoint_scores = predictions['keypoint_scores'][-6:]
        confidence = sum(keypoint_scores) / len(keypoint_scores)

        keypoints_with_occlusion = []
        for [x_coord, y_coord], score in zip(keypoints, keypoint_scores):
        # Translate keypoints to original image coordinates
            keypoints_with_occlusion.append([
                x_coord + x,
                y_coord + y,
                1 if score < 0.5 else 2
            ])

        # create updated annotation
        updated_ann = ann
        updated_ann['confidence_scores'] = (17 * [1.0]) + keypoint_scores
        updated_ann['keypoints'][-18:] = keypoints_with_occlusion
        
        mark = "need_manual_labeling" if confidence < 0.5 else "completed"
        markings[mark]['images'].append(image_id)
        markings[mark]['annotations'].append(updated_ann)

        os.remove(cropped_image_path)

    # finally:
    # save completed to completed directory
    # save manual labelling to manual_labelling directory
    print(f"Completed running inference on {len(annotations)} annotations.")
    for mark, v in markings.items():
        print(f"{mark}: {len(v['annotations'])} anns, {len(v['annotations']) / len(annotations):.1%}")
        images = set(v['images'])
        data['annotations'] = v['annotations']
        # save only the images that are in this split
        data['images'] = [img for img in all_images if img['id'] in images]
        
        save_dir = PIPELINE_DIR / SPLIT / mark / next_batch_dir.name
        os.makedirs(save_dir, exist_ok=True)
        with open(save_dir / "person_keypoints.json", 'w') as f:
            json.dump(data, f)

        if mark == "need_manual_labeling":
            # Zip and copy images
            image_paths = [image_dir / f'{image_id:012d}.jpg' for image_id in images]
            zip_and_copy_images(image_paths, save_dir)

    # update progress
    try:
        new_name = sorted_batches[sorted_batches.index(next_batch_dir.name) + 1]
    except IndexError:
        new_name = None

    progress[SPLIT]['next_batch_name'] = new_name
    progress[SPLIT]['completed'] += 1
        
    with open(progress_path, 'w') as f:
        json.dump(progress, f) 

    
    
if __name__ == '__main__':
    main()