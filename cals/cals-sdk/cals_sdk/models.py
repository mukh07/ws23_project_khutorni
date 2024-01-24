import json

from .data import Serializable


class Model(Serializable):
    """
    Metadata for a specific model.

    This class represents detailed information associated with a model,
    including its name, a list of its variants, and the configuration files
    for each variant.
    """

    def __init__(self, name: str = '', variant_keys: list = [],
                 variant_names: list = [], configs: list = []) -> None:
        super().__init__({
            "name": name,
            "variant_keys": variant_keys,
            "variant_names": variant_names,
            "configs": configs,
        })

    def get_variant_name(self, variant: str):
        """
        Get the name of a specific variant of the model.

        Args:
            variant (str): The name of the variant.

        Returns:
            str: The name of the variant.
        """
        key = self.variant_keys.index(variant)
        return self.variant_names[key]

    def get_variant_config(self, variant: str):
        """
        Get the configuration file for a specific variant of the model.

        Args:
            variant (str): The name of the variant.

        Returns:
            str: The path to the configuration file for the variant.
        """
        key = self.variant_keys.index(variant)
        return self.configs[key]


class Models:
    _instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if Models._instance is not None:
            raise Exception("This class is a singleton!")

        with open('configs/metadata.json') as json_file:
            json_data = json.load(json_file)
            metadata = []
            for meta_d in json_data:
                dataset = Dataset(**meta_d)
                metadata.append(dataset)

        self.metadata = metadata
        Models._instance = self

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Models._instance is None:
            Models._instance = Models()

        return Models._instance

    def list(self):
        """
        List the models.

        Returns:
            list: A list of the models.
        """
        return self.metadata

    def get(self, dataset: str):
        return next((d for d in self.metadata if d.name == dataset), None)

    def get_config(self, dataset: str, model: str):
        d = self.get(dataset)
        if d is None:
            return None

        m = next((m for m in d.models if m[0] == model), None)
        if m is None:
            return None

        return m[2]
