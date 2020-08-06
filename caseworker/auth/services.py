from caseworker.conf.client import post
from caseworker.conf.constants import AUTHENTICATION_URL


def authenticate_gov_user(request, json):
    data = post(request, AUTHENTICATION_URL, json)
    return data.json(), data.status_code
