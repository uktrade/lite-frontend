from http import HTTPStatus

from core import client
from caseworker.flags.enums import FlagStatus
from lite_content.lite_internal_frontend import open_general_licences


def get_open_general_licences(
    request, page=1, name=None, case_type=None, control_list_entry=None, country=None, status="active"
):
    querystring = convert_parameters_to_query_params(
        {
            "page": page,
            "name": name,
            "case_type": case_type,
            "control_list_entry": control_list_entry,
            "country": country,
            "status": status,
        }
    )
    return client.get(request, f"/open-general-licences/{querystring}").json()


def post_open_general_licences(request, json):
    response = client.post(request, "/open-general-licences/", json)
    return response.json(), response.status_code


def get_open_general_licence(request, pk):
    return client.get(request, f"/open-general-licences/{pk}").json()


def patch_open_general_licence(request, pk, json):
    response = client.patch(request, f"/open-general-licences/{pk}", json)
    return response.json(), response.status_code


def set_open_general_licence_status(request, pk, json):
    if "status" not in json:
        return {"errors": {"response": [open_general_licences.Edit.SELECT_OPTION]}}, HTTPStatus.BAD_REQUEST

    response = client.patch(request, f"/open-general-licences/{pk}", json)
    return response.json(), response.status_code


def get_ogl_activity(request, pk, activity_filters=None):
    url = f"/open-general-licences/{pk}/activity/"
    if activity_filters:
        params = convert_parameters_to_query_params(activity_filters)
        url = url + params
    data = client.get(request, url)
    return data.json()
