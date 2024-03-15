import json

SPLIT = "val2017"

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def check_annotations(original_file, new_file):
    coco = load_json(original_file)
    coco_ext = load_json(new_file)

    # TODO: Check all dictionary keys are same
    assert set(coco.keys()) == set(coco_ext.keys())

    # Check the individual annotations
    annos = coco['annotations']
    annos_ext = coco_ext['annotations']

    orig_map = { f"{ann['image_id']}-{ann['id']}": ann for ann in annos }

    invalid = 0
    valid = 0
    for ann in annos_ext:
        # TODO: Check that, if this is present in annos,
        #       then it should have the same 'image_id', same 'id',
        #       and same values for the first 17 keypoints.
        ann_orig = orig_map[f"{ann['image_id']}-{ann['id']}"]
        if ann_orig:
            valid += 1
            assert all(
                k_orig == k_ext 
                for k_orig, k_ext in zip(ann_orig['keypoints'], ann['keypoints'])
            )
        else:
            invalid += 1

    print(invalid, valid, invalid+valid)


check_annotations(
    f'../data/coco/annotations/person_keypoints_{SPLIT}.json', 
    f'../data/coco-extended/person_keypoints_{SPLIT}.json'
)