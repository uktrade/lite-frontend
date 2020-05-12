from core.helpers import convert_parameters_to_query_params
from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import PICKLIST_URL


def get_picklists_list(request, type, disable_pagination=False):
    response = get(request, PICKLIST_URL + convert_parameters_to_query_params(locals()))
    return response.json()


def get_picklists_for_input(request, picklist_type, show_deactivated=False, convert_to_options=False):
    data = get(
        request,
        PICKLIST_URL
        + "?type="
        + picklist_type
        + "&show_deactivated="
        + str(show_deactivated)
        + "&disable_pagination=True",
    ).json()["results"]

    if convert_to_options:
        options = []

        for item in data:
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
