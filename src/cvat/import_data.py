from cvat_sdk import make_client, models
from cvat_sdk.core.proxies.tasks import ResourceType, Task
from cvat_sdk.api_client.exceptions import NotFoundException
from dotenv import load_dotenv

import os
from pathlib import Path


load_dotenv()

PROJECT_ID = 21
CVAT_HOST = "http://mindgarage26.cs.uni-kl.de"
CVAT_PORT = 8080
CVAT_USER = os.getenv('CVAT_USER')
CVAT_PW = os.getenv('CVAT_PW')
ASSIGNEE_ID = int(os.getenv('ASSIGNEE_ID'))
SPLIT = "train"


def import_data(batch_path: Path, project_id: int):
    # TODO: Use CVAT SDK to:
    # (1) Check that the project exists
    # (2) Create a new task (this will return a task ID)
    # (3) Upload the images and annotations to this task
    # See SDK documentation to learn how to do this
    # https://opencv.github.io/cvat/docs/api_sdk/sdk/
    #
    # This function assumes that the project has the appropriate
    # labels (skeleton set up already)

    # When I call
    # import_data(paths, project_id)
    # a new task should appear on CVAT
    # with all the images from the ZIP file visible
    # AND annotations showing on the images

    # Create a Client instance bound to a local server and authenticate using basic auth
    with make_client(host=CVAT_HOST, port=CVAT_PORT, credentials=(CVAT_USER, CVAT_PW)) as client:
        try:
            # check whether project exists
            project = client.projects.retrieve(project_id)

            batch_name = batch_path.name
            batches_in_split = sorted(f for f in batch_path.parent.iterdir())
            batch_index = batches_in_split.index(batch_path)

            task_spec = {
                "name": f"{SPLIT}_b{batch_index}__{batch_name}",
                "project_id": project_id,
                "assignee_id": ASSIGNEE_ID
            }

            task = client.tasks.create_from_data(
                spec=task_spec,
                resource_type=ResourceType.LOCAL,
                resources=[batch_path / "images.zip"],
                annotation_path=str(batch_path / "person_keypoints.json"),
                annotation_format="COCO Keypoints 1.0"
            )
            print(f"Created task {task.id} | Size: {task.size}")

        except NotFoundException as e:
            print(f"Project with ID: {project_id} not found.")


if __name__ == "__main__":
    _batch_path = Path("/home/khutorni/project/ws23_project_khutorni/data/coco-extended/train2017/000000000036-000000009941")

    import_data(_batch_path, PROJECT_ID)
