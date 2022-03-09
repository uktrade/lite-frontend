from core import client
from core.helpers import convert_dict_to_query_params

from exporter.core.constants import SUPER_USER_ROLE_ID


def get_user(request, pk=None, params=None):
    if pk:
        url = f"/users/{pk}"
    else:
        url = "/users/me/"
    if params:
        url = url + "?" + convert_dict_to_query_params(params)
    return client.get(request, url).json()


def post_users(request, json):
    data = client.post(request, "/users/", json)
    return data.json(), data.status_code


def update_user(request, pk, json):
    data = client.put(request, f"/users/{pk}/", json)
    return data.json(), data.status_code


def is_super_user(user):
    return user["role"]["id"] == SUPER_USER_ROLE_ID
