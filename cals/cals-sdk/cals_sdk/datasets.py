from .data import Serializable
from .models import Model


class Dataset(Serializable):
    """ 
    Metadata for a specific dataset.

    This class represents detailed information associated with a dataset, 
    including its name, number of keypoints, the path to its skeleton file, 
    and a list of models available for the dataset.

    Args:
        name (str): The name of the dataset.
        num_keypoints (int): The number of keypoints in the dataset.
        skeleton_file (str): The path to the skeleton file associated with the dataset.
        models (list): A list of models available for the dataset.
    """

    def __init__(self, name: str = '',
                 num_keypoints: int = -11,
                 skeleton_file: str = '',
                 models: list = []) -> None:
        models_metadata = []
        for m in models:
            m = Model(**m)
            m_variant_keys = m.variant_keys
            m_variant_names = m.variant_names
            m_configs = m.configs

            for k, n, c in zip(m_variant_keys, m_variant_names, m_configs):
                models_metadata.append((k, n, c))

        super().__init__({
            "name": name,
            "num_keypoints": num_keypoints,
            "skeleton_file": skeleton_file,
            "models": models_metadata,
        })
