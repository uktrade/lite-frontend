from http import HTTPStatus
from urllib.parse import urlencode

from django.http import StreamingHttpResponse

from core.helpers import convert_parameters_to_query_params, convert_value_to_query_param
from lite_content.lite_exporter_frontend.generic import Document
from lite_forms.components import Option, TextArea

from conf.client import get, post, put, delete
from conf.constants import (
    UNITS_URL,
    APPLICATIONS_URL,
    STATIC_COUNTRIES_URL,
    EXTERNAL_LOCATIONS_URL,
    NOTIFICATIONS_URL,
    ORGANISATIONS_URL,
    CONTROL_LIST_ENTRIES_URL,
    NEWLINE,
    PV_GRADINGS_URL,
    ITEM_TYPES_URL,
    STATIC_F680_CLEARANCE_TYPES_URL,
)
from lite_forms.generators import error_page


def get_units(request, units=[]):  # noqa
    if units:
        return units
    data = get(request, UNITS_URL).json().get("units")
    for key, value in data.items():
        units.append(Option(key, value))
    return units


def get_country(request, pk):
    return get(request, STATIC_COUNTRIES_URL + pk).json()


def get_item_types(request):
    data = get(request, ITEM_TYPES_URL).json().get("item_types")
    options = []
    for key, value in data.items():
        if key == "other":
            options.append(
                Option(
                    key=key, value=value, components=[TextArea(name="other_item_type", extras={"max_length": 100},),],
                )
            )
        else:
            options.append(Option(key=key, value=value))
    return options


def get_countries(request, convert_to_options=False, exclude: list = None):
    """
    Returns a list of GOV.UK countries and territories
    param exclude: Takes a list of country codes and excludes them
    """

    data = get(request, STATIC_COUNTRIES_URL + "?" + convert_value_to_query_param("exclude", exclude)).json()[
        "countries"
    ]

    if convert_to_options:
        return [Option(x["id"], x["name"]) for x in data]

    return data


def get_sites_on_draft(request, pk):
    data = get(request, APPLICATIONS_URL + str(pk) + "/sites/")
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + "/sites/", json)
    return data.json(), data.status_code


def get_external_locations(request, pk, convert_to_options=False, exclude: list = None):
    data = get(
        request,
        ORGANISATIONS_URL + str(pk) + EXTERNAL_LOCATIONS_URL + "?" + convert_value_to_query_param("exclude", exclude),
    )

    if convert_to_options:
        external_locations_options = []

        for external_location in data.json().get("external_locations"):
            external_location_id = external_location.get("id")
            external_location_name = external_location.get("name")
            external_location_address = (
                external_location.get("address") + NEWLINE + external_location.get("country").get("name")
            )

            external_locations_options.append(
                Option(external_location_id, external_location_name, description=external_location_address)
            )

        return external_locations_options

    return data.json(), data.status_code


def get_external_locations_on_draft(request, pk):
    data = get(request, APPLICATIONS_URL + str(pk) + "/external_locations/")
    return data.json(), data.status_code


def delete_external_locations_from_draft(request, pk, ext_loc_pk):
    data = delete(request, APPLICATIONS_URL + pk + "/external_locations/" + ext_loc_pk + "/")
    return data.status_code


def post_external_locations_on_draft(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + "/external_locations/", json)
    return data.json(), data.status_code


def post_external_locations(request, pk, json):
    data = post(request, ORGANISATIONS_URL + str(request.user.organisation) + EXTERNAL_LOCATIONS_URL, json)

    if "errors" in data.json():
        return data.json(), data.status_code

    # Append the new external location to the list of external locations rather than clearing them
    _id = data.json()["external_location"]["id"]
    data = {"external_locations": [_id], "method": "append_location"}
    return post_external_locations_on_draft(request, str(pk), data)


def get_notifications(request):
    data = get(request, NOTIFICATIONS_URL)
    return data.json(), data.status_code


# Organisation
def get_organisations(request, page: int = 1, search_term=None, org_type=None):
    """
    Returns a list of organisations
    :param request: Standard HttpRequest object
    :param page: Returns n page of page results
    :param search_term: Filter by name
    :param org_type: Filter by org type - 'hmrc', 'commercial', 'individual', or an array of it
    """
    data = get(request, ORGANISATIONS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_organisation(request, pk):
    """
    Returns an organisation
    """
    data = get(request, ORGANISATIONS_URL + str(pk))
    return data.json()


def get_organisation_users(request, pk, params, convert_to_options=False):
    response = get(request, ORGANISATIONS_URL + str(pk) + "/users/?" + urlencode(params))

    if convert_to_options:
        options = []

        for user in response.json():
            title = user["first_name"] + " " + user["last_name"] if user["first_name"] else user["email"]
            description = user["email"] if user["first_name"] else ""

            options.append(Option(user["id"], title, description))

        return options

    return response.json()


def get_organisation_user(request, pk, user_pk):
    data = get(request, ORGANISATIONS_URL + pk + "/users/" + user_pk)
    return data.json()


def put_organisation_user(request, user_pk, json):
    organisation_id = str(request.user.organisation)
    data = put(request, ORGANISATIONS_URL + organisation_id + "/users/" + str(user_pk) + "/", json)
    return data.json(), data.status_code


def get_control_list_entries(request, convert_to_options=False, converted_control_list_entries_cache=[]):  # noqa
    if convert_to_options:
        if converted_control_list_entries_cache:
            return converted_control_list_entries_cache
        else:
            data = get(request, CONTROL_LIST_ENTRIES_URL + "?flatten=True")

        for control_list_entry in data.json().get("control_list_entries"):
            converted_control_list_entries_cache.append(
                Option(
                    key=control_list_entry["rating"],
                    value=control_list_entry["rating"],
                    description=control_list_entry["text"],
                )
            )

        return converted_control_list_entries_cache

    data = get(request, CONTROL_LIST_ENTRIES_URL)
    return data.json().get("control_list_entries")


# F680 clearance types
def get_f680_clearance_types(request):
    data = get(request, STATIC_F680_CLEARANCE_TYPES_URL)
    return data.json().get("types")


# PV gradings
def get_pv_gradings(request, convert_to_options=False):
    if convert_to_options:
        data = get(request, PV_GRADINGS_URL)

        converted_units = []
        for pvg in data.json().get("pv_gradings"):
            for key in pvg:
                converted_units.append(Option(key=key, value=pvg[key],))
        return converted_units

    data = get(request, PV_GRADINGS_URL)
    return data.json().get("pv-gradings")


def get_control_list_entry(request, rating):
    data = get(request, CONTROL_LIST_ENTRIES_URL + rating)
    return data.json().get("control_list_entry")


def get_document_download_stream(request, url):
    response = get(request, url)
    if response.status_code == HTTPStatus.OK:
        return StreamingHttpResponse(response, content_type=response.headers._store["content-type"][1])
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        error = Document.ACCESS_DENIED
    else:
        error = Document.DOWNLOAD_ERROR
    return error_page(request, error)


def _register_organisation(request, json, _type):
    data = {
        "type": _type,
        "user": {"email": request.user.email,},
    }
    response = post(request, ORGANISATIONS_URL, {**json, **data})
    return response.json(), response.status_code


def register_commercial_organisation(request, json):
    return _register_organisation(request, json, "commercial")


def register_private_individual(request, json):
    return _register_organisation(request, json, "individual")
