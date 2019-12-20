import requests

from fixtures.env import env


def _get_api_url():
    environment = env("ENVIRONMENT").lower()

    if environment == "local":
        url = env("LITE_API_URL")
        if not url.endswith("/"):
            url = url + "/"
        return url

    return "https://lite-api-" + environment + ".london.cloudapps.digital/"


def get(appended_address: str, headers):
    return requests.get(_get_api_url() + appended_address, headers=headers)


def post(appended_address: str, json, headers):
    return requests.post(_get_api_url() + appended_address, json=json, headers=headers)


def put(appended_address: str, json, headers):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"
    return requests.put(_get_api_url() + appended_address, json=json, headers=headers)


def delete(appended_address: str, headers):
    return requests.delete(_get_api_url() + appended_address, headers=headers,)
