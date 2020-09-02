from http import HTTPStatus

from core import client


def get_end_user_advisory(request, pk):
    data = client.get(request, f"/queries/end-user-advisories/{pk}")
    if data.status_code == HTTPStatus.OK:
        return data.json().get("end_user_advisory"), data.json().get("case_id")
    else:
        return None, None


def get_end_user_advisories(request, params):
    data = client.get(request, "/queries/end-user-advisories/" + params)
    return data.json()


def post_end_user_advisories(request, json):
    data = client.post(request, "/queries/end-user-advisories/", json)
    return data.json(), data.status_code
