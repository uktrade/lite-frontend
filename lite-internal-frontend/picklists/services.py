from conf.client import get, post, put
from conf.constants import PICKLIST_URL


def get_picklists(request, picklist_type):
    data = get(request, PICKLIST_URL + '?type=' + picklist_type)
    return data.json(), data.status_code


def post_picklist_item(request, json):
    data = post(request, PICKLIST_URL, json)
    return data.json(), data.status_code


def get_picklist_item(request, pk):
    data = get(request, PICKLIST_URL + pk)
    return data.json(), data.status_code


def put_picklist_item(request, pk, json):
    data = put(request, PICKLIST_URL + pk + "/", json)
    return data.json(), data.status_code
