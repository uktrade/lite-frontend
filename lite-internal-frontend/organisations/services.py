from conf.client import post
from conf.constants import ORGANISATIONS_URL


def post_organisations(request, json):
    data = post(request, ORGANISATIONS_URL, json)
    return data.json(), data.status_code
