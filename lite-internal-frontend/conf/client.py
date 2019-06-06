import requests

from conf.settings import env


def get(request, appended_address):
    if request:
        # This is intentional, this will be changed in a future story
        return requests.get(env("LITE_API_URL") + appended_address)

    return requests.get(env("LITE_API_URL") + appended_address)


def post(request, appended_address, json):
    return requests.post(env("LITE_API_URL") + appended_address,
                         json=json)


def put(request, appended_address, json):
    return requests.put(env("LITE_API_URL") + appended_address,
                        json=json)


def delete(request, appended_address):
    return requests.delete(env("LITE_API_URL") + appended_address)
