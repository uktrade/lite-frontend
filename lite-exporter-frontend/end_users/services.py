from conf.client import get, post
from conf.constants import END_USER_ADVISORIES_URL


def get_end_user_advisory(request, pk):
    data = get(request, END_USER_ADVISORIES_URL + pk)
    return data.json()['end_user_advisory'], data.json()['case_id']


def get_end_user_advisories(request):
    data = get(request, END_USER_ADVISORIES_URL)
    return data.json()['end_user_advisories']


def post_end_user_advisories(request, json):
    data = post(request, END_USER_ADVISORIES_URL, json)
    return data.json(), data.status_code
