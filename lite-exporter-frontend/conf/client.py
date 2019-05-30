import requests

from conf.settings import env


def get(request, appended_address):
    if request:
        return requests.get(env("LITE_API_URL") + appended_address,
                            headers={'USER-ID': str(request.user.id)})

    return requests.get(env("LITE_API_URL") + appended_address)


def post(request, appended_address, json):
    return requests.post(env("LITE_API_URL") + appended_address,
                         json=json,
                         headers={'USER-ID': str(request.user.id)})


def put(request, appended_address, json):
    return requests.put(env("LITE_API_URL") + appended_address,
                        json=json,
                        headers={'USER-ID': str(request.user.id)})


def delete(request, appended_address):
    return requests.delete(env("LITE_API_URL") + appended_address,
                           headers={'USER-ID': str(request.user.id)})
