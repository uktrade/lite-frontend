from conf.client import get, post, put
from conf.constants import USERS_URL, SUPER_USER_ROLE_ID


def get_user(request, pk=None, params=None):
    if pk:
        url = USERS_URL + str(pk)
    else:
        url = USERS_URL + "me/"
    if params:
        from core.helpers import convert_dict_to_query_params

        url = url + "?" + convert_dict_to_query_params(params)

    return get(request, url).json()


def post_users(request, json):
    data = post(request, USERS_URL, json)
    return data.json(), data.status_code


def update_user(request, pk, json):
    data = put(request, USERS_URL + pk + "/", json)
    return data.json(), data.status_code


def is_super_user(user):
    return user["role"]["id"] == SUPER_USER_ROLE_ID
