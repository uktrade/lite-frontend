from conf.client import get, post, put
from conf.constants import DEPARTMENTS_URL


def get_departments(request):
    data = get(request, DEPARTMENTS_URL)
    return data.json(), data.status_code


def post_departments(request, json):
    data = post(request, DEPARTMENTS_URL, json)
    return data.json(), data.status_code


def get_department(request, pk):
    data = get(request, DEPARTMENTS_URL + pk)
    return data.json(), data.status_code


def update_department(request, pk, json):
    data = put(request, DEPARTMENTS_URL + pk + "/", json)
    return data.json(), data.status_code
