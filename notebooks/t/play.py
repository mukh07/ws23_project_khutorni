from cals_sdk import CVATClient, Workflows
from cals_sdk.al import ActiveLearningWorkflow


# Authenticate with the server
import os
os.environ['CVAT_HOST'] = 'http://mindgarage26.cs.uni-kl.de:8080'
client = CVATClient.get_instance()
client.authenticate('khutorni', 'digitaltwin001')
print("Authenticated")

workflows = ActiveLearningWorkflow.get_all_workflows_metadata()
print(workflows)

workflow = ActiveLearningWorkflow(
    client,
    root='data/coco/val2017',
    anno_file='data/coco-extended/fixed_person_keypoints_val2017.json',
    model="/home/khutorni/project/ws23_project_khutorni/configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py",
    batch_size=100, # number of images to be annotated in one batch
    project_id=21, # project id
    work_dir='data/coco-extended-t3/',
)

# Select initial batch
# batch_idx, images_zip, anno_file = workflow.select_next_batch()
# print("Selected initial batch: ", batch_idx, images_zip, anno_file)
#
# # # Filter batch for stuff that is not inside
# bad_images_zip, bad_anno_file = workflow.filter_batch(batch_idx, images_zip, anno_file)
#
# # Upload task data to CVAT
# # workflow.upload_batch(bad_images_zip, bad_anno_file)
# task_id = workflow.upload_batch(bad_images_zip, bad_anno_file)

# what do I do after that??????
# run training again?

