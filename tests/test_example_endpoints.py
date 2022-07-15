"""
Test magic links functionality
"""
import pytest
from tests.utils import compare_events

@pytest.mark.usefixtures("flask_test_client")
class TestEventEndpoints:

    events = []

    def test_event_is_created(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /events with and json payload
        which includes the full event payload
        THEN an event record is created and returned
        :param flask_test_client:
        """
        expected_event = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_AMENDED",
                "timestamp": "2021-12-12 21:12:04",
                "user_id": "user123",
                "body": "{'key': 'body'}"
              }
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_AMENDED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": { "key": "body" }
              }
        endpoint = "/events"
        response = flask_test_client.post(endpoint, json=payload)
        response_event = response.get_json()
        self.events.append(response_event)
        assert response.status_code == 201
        compare_events(expected_event, response_event)

    def test_get_events_list(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /events
        THEN a list of event records is returned
        :param flask_test_client:
        """
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": {'key': 'a'}
              }
        payload_two = {
                "entity_identifier": "uuid2_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": {'key': 'b'}
              }
        endpoint = "/events"
        flask_test_client.post(endpoint, json=payload)
        flask_test_client.post(endpoint, json=payload_two)
        expected_events_list = [{
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "2021-12-12 21:12:04",
                "user_id": "user123",
                "body": "{'key': 'a'}"
              }, {
                "entity_identifier": "uuid2_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "2021-12-12 21:12:04",
                "user_id": "user123",
                "body": "{'key': 'b'}"
              }]
        response = flask_test_client.get(endpoint)
        response_events_list = response.get_json()

        assert response.status_code == 200
        for index, expected_event in enumerate(expected_events_list):
            compare_events(expected_event, response_events_list[index])

    def test_default_uuid_is_working(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /events twice with the same json payload
        THEN a different event id is set for each
        :param flask_test_client:
        """
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": { "key": "body" }
              }
        endpoint = "/events"
        response_one = flask_test_client.post(endpoint, json=payload)
        event_one = response_one.get_json()
        response_two = flask_test_client.post(endpoint, json=payload)
        event_two = response_two.get_json()
        assert response_one.status_code == 201
        assert response_two.status_code == 201
        assert event_one["id"] != event_two["id"]

    def test_partial_event_payload_fails(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /events with a partial json payload
        THEN a 401 error message is returned
        :param flask_test_client:
        """
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "user_id": "user123",
                "body": { "key": "body" }
              }
        endpoint = "/events"
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 400
        assert (
            error_response.get("message")
            == f"'timestamp' is missing a value, a full event payload is required."
    )


    def test_get_events_list_filter(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we GET /events
        THEN a list of event records is returned
        :param flask_test_client:
        """
        expected_events = [{"key": "name", "value": "Bob"}]
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": {'key': 'a'}
              }
        payload_two = {
                "entity_identifier": "uuid2_from_external",
                "code": "SCORE_SUBMITTED",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": {'key': 'b'}
              }
        post_endpoint = "/events"
        search_endpoint = "/events?event_id=SCORE_CREATED"
        flask_test_client.post(post_endpoint, json=payload)
        flask_test_client.post(post_endpoint, json=payload_two)
        expected_events_list = [{
                "entity_identifier": "uuid_from_external",
                "code": "SCORE_CREATED",
                "timestamp": "2021-12-12 21:12:04",
                "user_id": "user123",
                "body": "{'key': 'a'}"
              }]
        response = flask_test_client.get(search_endpoint)
        response_events_list = response.get_json()

        assert response.status_code == 200
        assert len(response_events_list) == 1
        for index, expected_event in enumerate(expected_events_list):
            compare_events(expected_event, response_events_list[index])

    def test_unknown_event_code_fails(self, flask_test_client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /events with a json payload containing an unknown event code
        THEN a 401 error message is returned
        :param flask_test_client:
        """
        payload = {
                "entity_identifier": "uuid_from_external",
                "code": "unknown",
                "timestamp": "04-12-21-12-12-2021",
                "user_id": "user123",
                "body": { "key": "body" }
              }
        endpoint = "/events"
        response = flask_test_client.post(endpoint, json=payload)
        error_response = response.get_json()

        assert response.status_code == 400
        assert (
            error_response.get("message")
            == f"There was an problem with your request"
        )