import os

import requests

from fixtures.env import env


def _get_api_url():
    environment = env("ENVIRONMENT").lower()

    if environment == "local":
        return env("LITE_API_URL")

    return "https://lite-api-" + environment + ".london.cloudapps.digital/"


def get(appended_address, headers):
    return requests.get(_get_api_url() + appended_address, headers=headers)


def post(appended_address, json, headers):
    return requests.post(_get_api_url() + appended_address, json=json, headers=headers)


def put(appended_address, json, headers):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    return requests.put(_get_api_url() + appended_address, json=json, headers=headers)


def delete(appended_address, headers):
    return requests.delete(_get_api_url() + appended_address, headers=headers,)
