from .data import RemoteDatabase
from .skeletons import Skeletons


class Projects(RemoteDatabase):
    """ A class for interacting with the projects endpoint of the CVAT API. """

    def __init__(self):
        super().__init__('/projects')

    def add(self, name: str, owner_id: int, skeleton_type: str = 'coco') -> bool:
        if skeleton_type not in Skeletons:
            raise ValueError(
                f"Invalid skeleton type: {skeleton_type}, must be one of: {Skeletons.keys()}")

        project = super().add({
            'name': name,
            'owner_id': owner_id,
            'labels': [{
                'name': 'person',
                'type': 'skeleton',
            }]
        })
        # FIXME: This doesn't work, so we have to manually add the skeleton label
        #        in the CVAT UI for now
        skeleton = Skeletons[skeleton_type]
        label_id = self.get_labels(project)[0].id
        r = self._client.patch(f'/labels/{label_id}', {
            # 'sublabels': skeleton['sublabels'],
            'svg': skeleton['svg'],
        })
        r = self._client.patch(f'/labels/{label_id}', {
            'sublabels': skeleton['sublabels'],
            # 'svg': skeleton['svg'],
        })
        return project

    def list_filtered(self) -> list:
        """ Gets a list of all projects with a skeleton label. """
        projects = super().list()

        # Filter out projects that don't have a skeleton label
        # i.e., not pose estimation projects
        filtered_projects = []
        for project in projects:
            labels = self.get_labels(project)
            for label in labels:
                if label.type == 'skeleton':
                    filtered_projects.append(project)
                    break

        return filtered_projects

    def get_labels(self, project: dict):
        """ Get labels for a project. """
        labels_url = project['labels']['url']
        if labels_url is None:
            return []

        r = self._client.get(labels_url)
        if r is None:
            return []

        return r['results']
