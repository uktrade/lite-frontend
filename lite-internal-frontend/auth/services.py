from conf.client import post
from conf.constants import AUTHENTICATION_URL


def authenticate_gov_user(json):
    data = post(None, AUTHENTICATION_URL, json)
    return data.json(), data.status_code
