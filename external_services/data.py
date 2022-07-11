import json
import urllib.parse

import requests
from config import Config


def api_call(endpoint: str, method: str = "GET", params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if Config.USE_LOCAL_DATA:
        return local_api_call(endpoint, params, method)
    else:
        if method:
            if method == "POST":
                return requests.post(endpoint, json=params)
            elif method == "GET":
                req = requests.PreparedRequest()
                req.prepare_url(endpoint, params)
                return requests.get(req.url)


def get_data(endpoint: str, params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if Config.USE_LOCAL_DATA:
        return local_api_call(endpoint, params, "get")
    else:
        req = requests.PreparedRequest()
        req.prepare_url(endpoint, params)
        response = requests.get(req.url)
        if response.status_code == 200:
            return response.json()


def post_data(endpoint: str, params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if Config.USE_LOCAL_DATA:
        return local_api_call(endpoint, params, "post")
    else:
        response = requests.post(endpoint, json=params)
        if response.status_code in [200, 201]:
            return response.json()


def local_api_call(endpoint: str, params: dict = None, method: str = "get"):
    test_api_data_json_path = Config.TEST_API_METHOD_PATH.format(
        method=method.lower()
    )
    fp = open(test_api_data_json_path)
    api_data = json.load(fp)
    fp.close()
    query_params = "_"
    if params:
        query_params = urllib.parse.urlencode(params)
    if method.lower() == "post":
        if endpoint in api_data:
            post_dict = api_data.get(endpoint)
            if query_params in post_dict:
                return post_dict.get(query_params)
            else:
                return post_dict.get("_default")
    else:
        if params:
            endpoint = f"{endpoint}?{query_params}"
        if endpoint in api_data:
            return api_data.get(endpoint)
