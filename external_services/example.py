from dataclasses import dataclass
from typing import List

from config import Config
from external_services.data import get_data
from external_services.data import post_data


@dataclass
class Example(object):
    key: str
    value: str

    @staticmethod
    def from_json(data: dict):
        return Example(
            key=data.get("key"),
            value=data.get("value"),
        )


class ExampleError(Exception):
    """Exception raised for errors in EXAMPLE management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class ExampleMethods(Example):
    @staticmethod
    def list(**kwargs) -> List[Example]:
        """
        List examples from the database

        Args:
            kwargs (dict): keyword args

        Returns:
            A list of example objects
        """
        url = Config.EXAMPLE_STORE_API_HOST + Config.EXAMPLES_ENDPOINT
        response = get_data(url, kwargs)

        if response:
            return [Example.from_json(item) for item in response]

    @staticmethod
    def get_example(key: str) -> Example:
        """
        Get an example from an external service
        corresponding to a given key

        Args:
            key (str): The example key

        Returns:
            Example object or raises an ExampleError if none found
        """
        url = Config.EXAMPLE_STORE_API_HOST + Config.EXAMPLE_ENDPOINT
        params = {"key": key}
        response = get_data(url, params)

        if response and "key" in response:
            return Example.from_json(response)

    @staticmethod
    def create_example(key: str, value: str) -> Example | None:
        """
        Create a new example if none exists

        Args:
            key (str): The example key
            value (str): The example value

        Returns:
            Example object or None
        """
        url = Config.EXAMPLE_STORE_API_HOST + Config.EXAMPLES_ENDPOINT
        params = {
            "key": key,
            "value": value,
        }
        response = post_data(url, params)

        if response and "key" in response:
            return Example.from_json(response)
