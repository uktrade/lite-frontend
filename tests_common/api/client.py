import os

import requests


LITE_API_URL = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)


def get(appended_address, headers):
    return requests.get(LITE_API_URL + appended_address, headers=headers)


def post(appended_address, json, headers):
    return requests.post(LITE_API_URL + appended_address, json=json, headers=headers)


def put(appended_address, json, headers):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    return requests.put(LITE_API_URL + appended_address, json=json, headers=headers)


def delete(appended_address, headers):
    return requests.delete(LITE_API_URL + appended_address, headers=headers,)
