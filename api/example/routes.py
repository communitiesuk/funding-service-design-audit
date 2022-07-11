import json

from api.responses import error_response
from api.responses import example_object_response
from db.models.example import ExampleError
from db.models.example import ExampleMethods
from flask import request
from flask import Response
from flask.views import MethodView


class ExamplesView(ExampleMethods, MethodView):
    def search(self, search_key: str = None):
        """
        GET /examples endpoint
        :param search_key: String key to search for
        :return: Json Response
        """
        return Response(
            json.dumps(self.list_examples(query=search_key, as_json=True)),
            mimetype="application/json",
        )

    def get(self, key: str):
        """
        GET /examples/{key} endpoint
        :param key: String key
        :return: example object json or 404 Error
        """
        try:
            example = self.get_example(key)
            return example_object_response(example.as_json(), 200)
        except ExampleError as e:
            return error_response(404, e.message)

    def create(self):
        """
        POST /examples endpoint
        :param key: the example key
        :param value: the example value
        :return: a json of the example object created (or an error of failure)
        """
        key = request.get_json().get("key")
        value = request.get_json().get("value")
        if not key or not value:
            return error_response(400, "key and value are required")
        try:
            new_example = self.create_example(key, value)
            return example_object_response(new_example.as_json(), 201)
        except ExampleError as e:
            return error_response(401, e.message)
