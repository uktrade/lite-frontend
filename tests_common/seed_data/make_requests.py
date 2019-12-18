import requests
from requests import request

from conf.settings import env


def make_request(method, base_url, url, headers, body=None, files=None):
    if body:
        response = request(method, base_url + url, json=body, headers=headers, files=files)
    else:
        response = request(method, base_url + url, headers=headers)

    if not response.ok:
        raise Exception("bad response: " + response.text)

    return response


def get(appended_address, headers):
    return requests.get(env("LITE_API_URL") + appended_address, headers=headers)


def post(appended_address, json, headers):
    return requests.post(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers=headers
    )


def put(appended_address, json, headers):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    return requests.put(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers=headers
    )


def delete(appended_address, headers):
    return requests.delete(
        env("LITE_API_URL") + appended_address,
        headers=headers,
    )
