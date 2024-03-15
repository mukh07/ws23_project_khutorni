from cals_sdk import CVATApiClient


class RemoteDatabase:
    """ Interface between the CVAT client and the application.

    This class provides a simple interface for storing and retrieving data from specific
    endpoints in the CVAT API. It provides methods to list, add, get details of, and delete
    items from the host using the CVAT client.

    Attributes:
        _client (CVATApiClient): The CVAT client to use for making requests to the API.
        _endpoint (str): The endpoint of the API. This is the URL path that will be appended
                         to the base URL of the CVAT client. For example, '/projects' will
                         be appended to 'http://localhost:8080/api' to make a request to
                         'http://localhost:8080/api/projects'.
    """
    SUPPORTED_ENDPOINTS = [
        '/projects',
        '/tasks',
        '/jobs',
        '/users',
    ]

    def __init__(self, endpoint: str):
        """ Initializes the RemoteDatabase object.

        Args:
            endpoint (str): The endpoint of the API.
        """
        assert isinstance(endpoint, str), 'endpoint must be a str'
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        assert endpoint in self.SUPPORTED_ENDPOINTS, \
            f'endpoint must be one of {self.SUPPORTED_ENDPOINTS}'

        self._endpoint = endpoint
        self._client = CVATApiClient.get_instance()

    def add(self, item: dict) -> dict or None:
        """ Adds an item to the CVAT endpoint.

        Args:
            item (dict): The item to be added to the database.

        Returns:
            dict or None: The response from the CVAT endpoint if the item was added
                          successfully, None otherwise.
        """
        assert isinstance(item, dict), 'item must be a dict'
        response = self._client.post(self._endpoint, item)
        return response

    def get(self, id: str) -> dict or None:
        """ Gets the details of an item from the CVAT endpoint.

        Args:
            id (str): The ID of the item to get details of.

        Returns:
            dict or None: The details of the item if it exists, None otherwise.
        """
        return self._client.get(f'{self._endpoint}/{id}')

    def list(self) -> list:
        """ Gets a list of all items in the CVAT endpoint.

        Returns:
            list: A list of all items in the database as dicts or an empty list
                  if there are no items.
        """
        items = []

        response = self._client.get(self._endpoint)
        if response is not None:
            count = response.count
            next = response.next
            items.extend(response.results)

            while next and len(items) < count:
                response = self._client.get(next)
                if response is None or len(response.results) == 0:
                    break

                items.extend(response.results)
                next = response.next

        return items

    def __len__(self) -> int:
        """ Gets the number of items in the CVAT endpoint.

        Returns:
            int: The number of items in the database.
        """
        response = self._client.get(self._endpoint)
        return response.count if response is not None else 0
