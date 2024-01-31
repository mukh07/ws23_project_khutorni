import json
import os

from .serializable import Serializable


class JsonDatabase:
    """A JSON-based database.

    Attributes:
        json_path (str): The path to the JSON file.
        data (list): The list of dictionaries to be stored as JSON data.
    """

    def __init__(self, json_path: str):
        """
        Args:
            json_path (str): The path to the JSON file.
        """
        self.json_path = json_path
        if not os.path.exists(json_path):
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            self.data = []
            self.update_db()
        else:
            with open(json_path, "r") as json_file:
                self.data = json.load(json_file)

    def add(self, item: Serializable):
        """Adds an item to the database and updates the JSON file.

        Args:
            item (Serializable): The item to be added.
        """
        self.data.append(item.to_dict())
        self.update_db()

    def get(self, key: str, value: str) -> Serializable:
        """Finds and returns a dictionary from the database that matches a specific key-value pair.

        Args:
            key (str): The key to be matched.
            value (str): The value to be matched.

        Returns:
            Serializable: The item that matches the key-value pair. None if no match is found.
        """
        for item in self.data:
            if item.get(key) == value:
                return Serializable(item)
        return None

    def delete(self, key: str, value: str):
        keep = []
        for item in self.data:
            if item.get(key) != value:
                keep.append(item)
        self.data = keep
        self.update_db()

    def list(self) -> list:
        """Returns the list of dictionaries in the database.

        Returns:
            list: The list of items in the database.
        """
        items = [Serializable(i) for i in self.data]
        return items

    def __len__(self) -> int:
        """Returns the number of dictionaries in the database.

        Returns:
            int: The number of dictionaries in the database.
        """
        return len(self.data)

    def update_db(self):
        """Updates the JSON file with the current data in the database."""
        with open(self.json_path, mode='w') as json_file:
            json.dump(self.data, json_file, indent=4, sort_keys=True)
