"""
Test magic links functionality
"""
import pytest


@pytest.mark.usefixtures("flask_test_client")
class TestExampleEndpoints:

    examples = []

    def test_example_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /examples with and json payload
        which includes a key and value
        THEN an example record is created and returned
        :param flask_test_client:
        """
        expected_response = {"key": "name", "value": "Bob"}
        payload = {"key": "name", "value": "Bob"}
        endpoint = "/examples"
        response = flask_test_client.post(endpoint, json=payload)
        example = response.get_json()
        self.examples.append(example)

        assert response.status_code == 201
        assert example == expected_response

    def test_create_duplicate_example_key_fails(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /examples with and json payload
        which includes a key that already has been set
        THEN a 401 error message is returned
        :param flask_test_client:
        """
        payload = {"key": "name", "value": "Bob"}
        endpoint = "/examples"
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 401
        assert (
            error_response.get("message")
            == "An example with key 'name' already exists"
        )

    def test_get_examples_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /examples
        THEN a list of example records is returned
        :param flask_test_client:
        """
        expected_examples = [{"key": "name", "value": "Bob"}]
        endpoint = "/examples"
        response = flask_test_client.get(endpoint)
        examples_list = response.get_json()

        assert response.status_code == 200
        assert examples_list == expected_examples
