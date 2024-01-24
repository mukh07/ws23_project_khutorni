from .data import JsonDatabase, Serializable


class Workflow(Serializable):
    """ Workflow description.

    A workflow is a set of annotation tasks in a project with a specific
    model used for getting active learning suggestions for which images
    to annotate next in the dataset.
    """

    def __init__(self, project: str, model: str, data: str, tasks: list):
        """ Constructor.

        Args:
            project (str): The project id.
            model (str): The model name.
            data (str): The dataset id.
            tasks (list): The list of task ids.
        """
        super().__init__({
            'project': project,
            'model': model,
            'data': data,
            'tasks': tasks,
        })


class Workflows(JsonDatabase):
    def __init__(self, project_id: str):
        super().__init__(f'appdata/workflows/{project_id}.json')
