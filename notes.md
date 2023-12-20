1. coco = Load(coco2017_train.json)
2. mpii_model = LoadMPIIModel()
3. extended_annos = []
3. For anno in coco['annotations']:
   2.1 Get image name and bbox from anno
   2.2 Open the image from coco folder
   2.3 Crop the image (Use PIL)
   2.4 Save the cropped image in a temporary folder # image_id-id.png
   2.5 mpii_keypoints =  mpii_model(cropped_path) # 16 keypoints returned
   2.6 kpts_subset = SelectSpineKeypoints(mpii_keypoints)
   2.7 kpts_subset.append(InterpolateSpine(kpts_subset))
   2.8 anno['keypoints'].append(kpts_subset)
   2.9 extended_annos.append(anno)
4. Save extended_annos and other keys from original json to a new json.

5. Copy images from original dataset, save .zip and .json
Goal: successfully load data into CVAT