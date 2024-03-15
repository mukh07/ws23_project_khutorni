import logging
import os

import requests
from easydict import EasyDict as edict


class CVATApiClient:
    """ Client for interacting with the CVAT API.

    This is a singleton class for interacting with the CVAT API. It provides methods for making GET
    and POST requests to the API. It also provides methods for authenticating with the API and
    retrieving the authentication token.

    The user must call the authenticate method before making any requests to the API. The `CVAT_HOST`
    environment variable must be set to the base URL of the CVAT API. This is the URL that all
    requests are made to and should not include the `/api` prefix or a trailing slash. For example,
    if the CVAT API is running at `http://localhost:8080/api`, then the user should set the
    `CVAT_HOST` environment variable to `http://localhost:8080`.

    Attributes:
        _instance (CVATApiClient): The singleton instance of the CVATApiClient class.
        host (str): The base URL of the CVAT API.
        auth_token (str or None): The authentication token for the CVAT API. None if the client is
                                  not authenticated, otherwise a string. Defaults to None.

    Methods:
        get_instance() -> CVATApiClient:
            Returns the singleton instance of the CVATApiClient class.
    """
    _instance = None

    @staticmethod
    def get_instance():
        """ Get the singleton instance of the CVATApiClient class.

        The instance is created the first time this method is called and is reused for all
        subsequent calls. The user must set the `CVAT_HOST` environment variable before calling
        this method.

        Returns:
            CVATApiClient: The singleton instance of the CVATApiClient class.

        Raises:
            ValueError: If the `CVAT_HOST` environment variable is not set.
        """
        if CVATApiClient._instance is None:
            base_url = os.environ.get('CVAT_HOST')
            if not base_url or base_url.strip() == '':
                raise ValueError("Set the CVAT_HOST environment variable")

            CVATApiClient._instance = CVATApiClient(base_url)

        return CVATApiClient._instance

    def __init__(self, host: str) -> None:
        """ Virtually private constructor. """
        if CVATApiClient._instance is not None:
            raise Exception("This class is a singleton!")

        self.host = host.strip().rstrip('/')
        if not self.host.endswith(f'/api'):
            self.host += '/api'

        self._auth_token = "98c58fc22fd3b25bae973d138410782d0a7a1b04"  # None

    @property
    def auth_token(self) -> str or None:
        """ The authentication token for the CVAT API. None if the client is not authenticated,
        otherwise a string. """
        return self._auth_token

    @auth_token.setter
    def auth_token(self, value: str or None) -> None:
        """ Sets the authentication token for the CVAT API. """
        self._auth_token = value

    def _log_error(self, e: Exception) -> None:
        """ Logs an error message. """
        logging.error(f"CVATApiClient: {e}")
        import traceback
        logging.debug(traceback.format_exc())

    def authenticate(self, username, password) -> bool:
        """ Authenticate with the CVAT API.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.

        Returns:
            bool: True if authentication was successful, False otherwise.

        Raises:
            HTTPError: If the authentication fails because of a bad status code.
            Exception: If the authentication fails for any other reason.
        """
        # Get the authentication token
        api_url = f'{self.host}/auth/login'
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}
        response = requests.post(
            api_url, headers=headers, json=data, verify=True)
        response.raise_for_status()
        response = response.json()

        # Set the authentication token
        if 'key' not in response:
            raise Exception("Authentication failed")

        self.auth_token = response['key']
        return True

    def clear_auth_token(self) -> None:
        """ Clears the authentication token. """
        self.post('auth/logout', {})
        self.auth_token = None

    def get(self, path: str) -> edict or None:
        """ Make a GET request to the API.

        Args:
            path (str): The path of the API endpoint to make the request to.

        Returns:
            edict: The API response as an easydict or None if the request fails.

        Raises:
            Exception: If the client is not authenticated.
        """
        try:
            if self.auth_token is None:
                raise Exception("Not authenticated")

            if path.startswith(self.host):
                path = path[len(self.host):]

            if path.startswith('/'):
                path = path[1:]

            response = requests.get(
                f'{self.host}/{path}',
                headers={'Authorization': f'Token {self.auth_token}'},
                verify=True
            )
            response.raise_for_status()
            return edict(response.json())
        except Exception as e:
            self._log_error(e)
            return None

    def post(self, path: str, data: dict) -> edict or None:
        """ Make a POST request to the API. 

        Args:
            path (str): The path of the API endpoint to make the request to.
            data (dict): The data to send with the request.

        Returns:
            dict: The API response as an easydict or None if the request fails.

        Raises:
            Exception: If the client is not authenticated.
        """
        try:
            if self.auth_token is None:
                raise Exception("Not authenticated")

            if path.startswith(self.host):
                path = path[len(self.host):]

            if path.startswith('/'):
                path = path[1:]

            response = requests.post(
                f'{self.host}/{path}',
                headers={'Content-Type': 'application/json',
                         'Authorization': f'Token {self.auth_token}'},
                json=data,
                verify=True
            )

            response.raise_for_status()
            return edict(response.json())
        except Exception as e:
            self._log_error(e)
            return None

    def patch(self, path: str, data: dict) -> edict or None:
        """ Make a PATCH request to the API.

        Args:
            path (str): The path of the API endpoint to make the request to.
            data (dict): The data to send with the request.

        Returns:
            dict: The API response as an easydict or None if the request fails.

        Raises:
            Exception: If the client is not authenticated.
        """
        try:
            if self.auth_token is None:
                raise Exception("Not authenticated")

            if path.startswith(self.host):
                path = path[len(self.host):]

            if path.startswith('/'):
                path = path[1:]

            response = requests.patch(
                f'{self.host}/{path}',
                headers={'Content-Type': 'application/json',
                         'Authorization': f'Token {self.auth_token}'},
                json=data,
                verify=True
            )

            response.raise_for_status()
            return edict(response.json())
        except Exception as e:
            self._log_error(e)
            return None
