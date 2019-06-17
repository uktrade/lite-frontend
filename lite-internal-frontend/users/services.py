from conf.client import get, post, put
from conf.constants import USERS_URL


def get_users(request):
    data = get(request, USERS_URL)
    return data.json(), data.status_code


def get_user(request, pk):
    data = get(request, USERS_URL + pk)
    return data.json(), data.status_code


def post_users(request, json):
    data = post(request, USERS_URL, json)
    return data.json(), data.status_code


def update_user(request, pk, json):
    data = put(request, USERS_URL + pk + "/", json)
    return data.json(), data.status_code
