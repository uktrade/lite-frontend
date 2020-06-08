from http import HTTPStatus

from conf.client import get, patch, post
from conf.constants import OPEN_GENERAL_LICENCES_URL, ACTIVITY_URL
from core.helpers import convert_parameters_to_query_params
from lite_content.lite_internal_frontend import open_general_licences


def get_open_general_licences(
    request, page=1, name=None, case_type=None, control_list_entry=None, country=None, status=None
):
    return get(request, OPEN_GENERAL_LICENCES_URL + convert_parameters_to_query_params(locals())).json()


def post_open_general_licences(request, json):
    response = post(request, OPEN_GENERAL_LICENCES_URL, json)
    return response.json(), response.status_code


def get_open_general_licence(request, pk):
    return get(request, OPEN_GENERAL_LICENCES_URL + str(pk)).json()


def patch_open_general_licence(request, pk, json):
    response = patch(request, OPEN_GENERAL_LICENCES_URL + str(pk), json)
    return response.json(), response.status_code


def set_open_general_licence_status(request, pk, json):
    if "status" not in json:
        return {"errors": {"response": [open_general_licences.Edit.SELECT_OPTION]}}, HTTPStatus.BAD_REQUEST

    response = patch(request, OPEN_GENERAL_LICENCES_URL + str(pk), json)
    return response.json(), response.status_code


def get_ogl_activity(request, pk, activity_filters=None):
    url = OPEN_GENERAL_LICENCES_URL + str(pk) + ACTIVITY_URL
    if activity_filters:
        params = convert_parameters_to_query_params(activity_filters)
        url = url + params
    data = get(request, url)
    return data.json()
