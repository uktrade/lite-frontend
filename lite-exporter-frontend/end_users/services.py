from http import HTTPStatus

from conf.client import get, post
from conf.constants import END_USER_ADVISORIES_URL


def get_end_user_advisory(request, pk):
    data = get(request, END_USER_ADVISORIES_URL + pk)
    if data.status_code == HTTPStatus.OK:
        return data.json().get("end_user_advisory"), data.json().get("case_id")
    else:
        return None, None


def get_end_user_advisories(request):
    data = get(request, END_USER_ADVISORIES_URL)
    return data.json().get("end_user_advisories") if data.status_code == HTTPStatus.OK else None


def post_end_user_advisories(request, json):
    data = post(request, END_USER_ADVISORIES_URL, json)
    return data.json(), data.status_code
