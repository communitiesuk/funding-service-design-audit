import json

from api.responses import error_response
from api.responses import event_object_response
from db.models.event import EventError
from db.models.event import EventMethods
from flask import request
from flask import Response
from flask.views import MethodView


class EventsView(EventMethods, MethodView):
    def search(self, event_id: str = None):
        """
        GET /events endpoint
        :param search_key: String key to search for
        :return: Json Response
        """
        return Response(
            json.dumps(self.list_events(query=event_id, as_dict=True)),
            mimetype="application/json",
        )

    def get(self, key: str):
        """
        GET /events/{key} endpoint
        :param key: String key
        :return: event object json or 404 Error
        """
        try:
            event = self.get_event(key)
            return event_object_response(event.as_json(), 200)
        except EventError as e:
            return error_response(404, e.message)

    def create(self):
        """
        POST /events endpoint
        :param key: the event key
        :param value: the event value
        :return: a json of the event object created (or an error of failure)
        """
        import datetime

        event_payload = {
            "code": request.get_json().get("code"),
            "entity_identifier": request.get_json().get("entity_identifier"),
            "timestamp": request.get_json().get("timestamp"),
            "user_id": request.get_json().get("user_id"),
            "body": str(request.get_json().get("body")),
        }
        for key, value in event_payload.items():
            if value is None:
                return error_response(
                    400,
                    f"'{key}' is missing a value, a full event payload is"
                    " required.",
                )
        try:
            event_payload["timestamp"] = datetime.datetime.strptime(
                event_payload["timestamp"], "%S-%M-%H-%d-%m-%Y"
            )
            new_event = self.create_event(**event_payload)
            return event_object_response(new_event.as_dict(), 201)
        except EventError as e:
            return error_response(e.code, e.message)
