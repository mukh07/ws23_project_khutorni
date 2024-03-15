import json

SPLIT = "train2017"

with open(f'../data/coco-extended/person_keypoints_{SPLIT}.json') as f:
    data = json.load(f)
    
fixed_anns = []
for ann in data['annotations']:
    bbox = ann['bbox']
    x, y, width, height = bbox

    # just like in generate_initial_dataset
    if width <= 0 or height <= 0:
        continue

    updated_kpts = []
    for i in range(len(ann['keypoints']) - 18, len(ann['keypoints']), 3):
        ann['keypoints'][i] += x
        ann['keypoints'][i + 1] += y
    fixed_anns.append(ann)


with open(f'../data/coco-extended/fixed_person_keypoints_{SPLIT}.json', "w") as f:
    data['annotations'] = fixed_anns
    json.dump(data, f)