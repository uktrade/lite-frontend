from http import HTTPStatus

from core import client
from core.helpers import convert_parameters_to_query_params
from lite_content.lite_internal_frontend.picklists import Picklists
from lite_forms.components import Option


def get_picklists_list(request, type, page=1, name=None, disable_pagination=False, show_deactivated=True):
    querystring = convert_parameters_to_query_params(
        {
            "type": type,
            "page": page,
            "name": name,
            "disable_pagination": disable_pagination,
            "show_deactivated": show_deactivated,
        }
    )
    response = client.get(request, f"/picklist/{querystring}")
    return response.json()


def get_picklists_for_input(request, picklist_type, show_deactivated=False, convert_to_options=False):
    data = client.get(
        request,
        f"/picklist/?type={picklist_type}&show_deactivated={show_deactivated}&disable_pagination=True",
    ).json()["results"]

    if convert_to_options:
        options = []

        for item in data:
            options.append(Option(item["id"], item["name"], item["text"]))

        return options

    return data


def post_picklist_item(request, json):
    data = client.post(request, "/picklist/", json)
    return data.json(), data.status_code


def get_picklist_item(request, pk):
    data = client.get(request, f"/picklist/{pk}")
    return data.json()["picklist_item"]


def put_picklist_item(request, pk, json):
    data = client.put(request, f"/picklist/{pk}", json)
    return data.json(), data.status_code


def set_picklist_item_status(request, pk, json):
    if "status" not in json:
        return {"errors": {"response": [Picklists.SELECT_OPTION]}}, HTTPStatus.BAD_REQUEST

    response = client.put(request, f"/picklist/{pk}", json)
    return response.json(), response.status_code
