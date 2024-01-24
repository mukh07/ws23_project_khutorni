import os
from typing import List

from cvat_sdk import Client
from cvat_sdk.core.proxies.tasks import ResourceType, Task
from cvat_sdk.core.proxies.projects import Project


class CVATClient(Client):
    _instance = None

    @staticmethod
    def get_instance():
        if CVATClient._instance is None:
            base_url = os.environ.get('CVAT_HOST')
            if not base_url or base_url.strip() == '':
                raise ValueError("Set the CVAT_HOST environment variable")

            CVATClient._instance = CVATClient(base_url)

        return CVATClient._instance

    def __init__(self, host: str) -> None:
        """ Virtually private constructor. """
        if CVATClient._instance is not None:
            raise Exception("This class is a singleton!")

        self.host = host.strip().rstrip('/')
        super().__init__(self.host)

    def authenticate(self, username, password) -> bool:
        super().login(credentials=(username, password))
        return self.has_credentials()

    def clear_auth_token(self) -> None:
        """ Clears the authentication token. """
        super().logout()

    def get_projects(self) -> List[Project]:
        if not self.has_credentials():
            raise ValueError("No credentials set")

        # TODO: List all projects owned by current user ONLY
        # See CVAT SDK docs for more info
        return []

    def get_assigned_projects(self) -> List[Project]:
        if not self.has_credentials():
            raise ValueError("No credentials set")

        # TODO: List all projects assigned to the current user ONLY
        # See CVAT SDK docs for more info
        return []

    def get_project_tasks(self, project_id: int) -> List[Task]:
        if not self.has_credentials():
            raise ValueError("No credentials set")

        project = self.projects.retrieve(project_id)
        return project.get_tasks()

    def get_task_data(self, task_id: int) -> Task:
        if not self.has_credentials():
            raise ValueError("No credentials set")

        # TODO: Get task data
        # See CVAT SDK docs for more info
        return None

    def upload_task_data(self, name, images_zip, annotations_file,
                         project_id: int, assignee_id=None):
        task_spec = {
            "name": name,
            "project_id": project_id,
            "assignee_id": assignee_id
        }

        task = self.tasks.create_from_data(
            spec=task_spec,
            resource_type=ResourceType.LOCAL,
            resources=[images_zip],
            annotation_path=str(annotations_file),
            annotation_format="COCO Keypoints 1.0"
        )

        return task.id
