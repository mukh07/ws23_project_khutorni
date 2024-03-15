import json

from easydict import EasyDict


class Serializable(EasyDict):
    """ A class that represents an item in a database.

    This class provides a dictionary-like object that allows access to its
    values using attribute syntax (i.e., `item.key` instead of `item['key']`).

    Args:
        data (dict): A dictionary containing the data for the database item.
    """

    def __init__(self, data: dict):
        super().__init__(data)

    @staticmethod
    def from_dict(data: dict):
        """ Creates a database item from a dictionary. """
        return Serializable(data)

    @staticmethod
    def from_json(json_string: str):
        """ Creates a database item from a JSON string. """
        return Serializable(json.loads(json_string))

    @staticmethod
    def from_file(file_path: str):
        """ Creates a database item from a JSON file. """
        with open(file_path, "r") as json_file:
            return Serializable.from_json(json_file.read())

    def to_dict(self) -> dict:
        """ Returns a dictionary representation of the database item. """
        return {k: v for k, v in self.items() if not callable(v)}

    def to_json(self) -> str:
        """ Serializes the database item to a JSON string. """
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_json()})"
