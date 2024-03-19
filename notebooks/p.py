from cals_sdk.al import ActiveLearningWorkflow


def create_al_workflow(client, home, batch_size, name, project_id):
    workflow = ActiveLearningWorkflow(
        client,
        root=f'data/coco/val2017',
        anno_file=f'data/coco-extended/fixed_person_keypoints_val2017.json',
        # model=f"{home}/configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py",
        model=f"configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py",
        batch_size=batch_size,  # number of images to be annotated in one batch
        project_id=project_id,  # project id
        work_dir=f'data/{name}/',
    )
    return workflow
