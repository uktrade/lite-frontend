from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import PICKLIST_URL


def get_picklists(request, picklist_type, show_deactivated=False, convert_to_options=False, include_none=False):
    data = get(request, PICKLIST_URL + "?type=" + picklist_type + "&show_deactivated=" + str(show_deactivated)).json()

    if convert_to_options:
        options = []

        if include_none:
            options.append(Option(None, "None", "None"))

        for item in data["picklist_items"]:
            options.append(Option(item["id"], item["name"], item["text"]))

        return options

    return data


def post_picklist_item(request, json):
    data = post(request, PICKLIST_URL, json)
    return data.json(), data.status_code


def get_picklist_item(request, pk):
    data = get(request, PICKLIST_URL + str(pk))
    return data.json()["picklist_item"]


def put_picklist_item(request, pk, json):
    data = put(request, PICKLIST_URL + str(pk) + "/", json)

    return data.json(), data.status_code
