import json
import os
import zipfile
import shutil
from itertools import chain, groupby

SPLIT = "train"
PATH = '../data/coco-extended'
FILENAME = f'{PATH}/fixed_person_keypoints_{SPLIT}2017.json'
SPLIT_FOLDER = f'{PATH}/{SPLIT}2017/'
IMAGE_ORIGINAL_FOLDER = f'../data/coco/{SPLIT}2017/'


def zip_and_copy_images(image_paths, destination_path):
    zip_filename = 'images.zip'

    # Create a ZIP archive containing the files
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_path in image_paths:
            # Add each file to the ZIP archive
            zipf.write(image_path, os.path.basename(image_path))

    # Move the ZIP archive to the destination directory
    shutil.move(zip_filename, os.path.join(destination_path, zip_filename))


def split_into_batches(batch_size=1000):
    """
    Split annotations into batches and write to separate files.
    """
    with open(FILENAME, 'r') as f:
        data = json.load(f)
        all_annotations = data['annotations']
        all_images = data['images']
        # print(all_annotations)

    # Group annotations by 'image_id'
    sorted_annotations = sorted(all_annotations, key=lambda x: x['image_id'])
    grouped_annotations = groupby(sorted_annotations, key=lambda x: x['image_id'])
    grouped_list = [(key, list(items)) for key, items in grouped_annotations]

    batch = []
    batch_count = 0

    for i, (key, annotations) in enumerate(grouped_list, start=1):
        # annotations = list(annotations)
        if i % batch_size == 0 or i == len(grouped_list):
            # Define path
            batch_name = f"{batch[0][0]:012d}-{batch[-1][0]:012d}"
            dir_path = os.path.join(SPLIT_FOLDER, batch_name)
            
            # Create folders
            os.makedirs(dir_path, exist_ok=True)
            
            # Write annotations to json file
            filename = os.path.join(dir_path, 'person_keypoints.json')
            batch_anns = list(chain.from_iterable(ann for (_, ann) in batch))

            new_data = {k: v for k, v in data.items() if k not in ['annotations', 'images']}                
            with open(filename, 'w') as f:
                new_data['annotations'] = batch_anns
                new_data['images'] = [img for img in all_images if img['id'] in [a['image_id'] for a in batch_anns]]
                json.dump(new_data, f)
            print(f'Written batch {batch_count + 1}: {batch_count * batch_size + 1}-{i}')

            # Zip and copy images
            image_paths = [
                os.path.join(IMAGE_ORIGINAL_FOLDER, f'{ann[0]:012d}.jpg')
                for ann in batch
            ]
            zip_and_copy_images(image_paths, dir_path)
        

            batch = []
            batch_count += 1

        batch.append((key, annotations))


if __name__ == '__main__':
    # Split into batches and write to files
    split_into_batches()
