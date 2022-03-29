from http import HTTPStatus
from urllib.parse import urlencode

from django.http import HttpResponse

from core import client

from core.helpers import convert_parameters_to_query_params, convert_value_to_query_param
from lite_content.lite_exporter_frontend.applications import OpenGeneralLicenceQuestions
from lite_forms.components import Option, TextArea


def get_units(request, units=[]):  # noqa
    if units:
        return units
    response = client.get(request, "/static/units/")
    response.raise_for_status()
    units = response.json()["units"]

    return units


def get_country(request, pk):
    return client.get(request, f"/static/countries/{pk}").json()


def get_item_types(request):
    data = client.get(request, "/static/item-types/").json().get("item_types")
    options = []
    for key, value in data.items():
        if key == "other":
            options.append(
                Option(
                    key=key,
                    value=value,
                    components=[
                        TextArea(
                            name="other_item_type",
                            extras={"max_length": 100},
                        ),
                    ],
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

    data = client.get(request, "/static/countries/?" + convert_value_to_query_param("exclude", exclude)).json()[
        "countries"
    ]

    if convert_to_options:
        return [Option(x["id"], x["name"]) for x in data]

    return data


def get_sites_on_draft(request, pk):
    data = client.get(request, f"/applications/{pk}/sites/")
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = client.post(request, f"/applications/{pk}/sites/", json)
    return data.json(), data.status_code


def get_external_locations(request, pk, convert_to_options=False, exclude: list = None, application_type: str = None):
    querystring = "&".join(
        [
            convert_value_to_query_param("exclude", exclude),
            convert_value_to_query_param("application_type", application_type),
        ]
    )

    data = client.get(request, f"/organisations/{pk}/external_locations/?{querystring}")

    if convert_to_options:
        external_locations_options = []

        for external_location in data.json().get("external_locations"):
            external_location_id = external_location.get("id")
            external_location_name = external_location.get("name")
            external_location_address = (
                (external_location.get("address") + "\n" + external_location.get("country").get("name"))
                if external_location.get("country")
                else external_location.get("address")
            )

            external_locations_options.append(
                Option(external_location_id, external_location_name, description=external_location_address)
            )

        return external_locations_options

    return data.json(), data.status_code


def get_external_locations_on_draft(request, pk):
    data = client.get(request, f"/applications/{pk}/external_locations/")
    return data.json(), data.status_code


def delete_external_locations_from_draft(request, pk, ext_loc_pk):
    data = client.delete(request, f"/applications/{pk}/external_locations/{ext_loc_pk}/")
    if data.status_code == HTTPStatus.BAD_REQUEST:
        return data.json(), data.status_code
    else:
        return {}, data.status_code


def post_external_locations_on_draft(request, pk, json):
    data = client.post(request, f"/applications/{pk}/external_locations/", json)
    return data.json(), data.status_code


def post_external_locations(request, pk, json):
    organisation_id = request.session["organisation"]
    data = client.post(request, f"/organisations/{organisation_id}/external_locations/", json)

    if "errors" in data.json():
        return data.json(), data.status_code

    # Append the new external location to the list of external locations rather than clearing them
    _id = data.json()["external_location"]["id"]
    data = {"external_locations": [_id], "method": "append_location"}
    return post_external_locations_on_draft(request, str(pk), data)


def get_notifications(request):
    data = client.get(request, "/users/notifications/")
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
    data = client.get(request, "/organisations/" + convert_parameters_to_query_params(locals()))
    return data.json()


def get_organisation(request, pk):
    """
    Returns an organisation
    """
    data = client.get(request, f"/organisations/{pk}")
    return data.json()


def get_organisation_users(request, pk, params, convert_to_options=False):
    response = client.get(request, f"/organisations/{pk}/users/?{urlencode(params)}")

    if convert_to_options:
        options = []

        for user in response.json():
            title = user["first_name"] + " " + user["last_name"] if user["first_name"] else user["email"]
            description = user["email"] if user["first_name"] else ""

            options.append(Option(user["id"], title, description))

        return options

    return response.json()


def get_organisation_user(request, pk, user_pk):
    data = client.get(request, f"/organisations/{pk}/users/{user_pk}")
    return data.json()


def put_organisation_user(request, user_pk, json):
    organisation_id = str(request.session["organisation"])
    data = client.put(request, f"/organisations/{organisation_id}/users/{user_pk}/", json)
    return data.json(), data.status_code


def get_control_list_entries(request, convert_to_options=False, converted_control_list_entries_cache=[]):  # noqa
    if convert_to_options:
        if converted_control_list_entries_cache:
            return converted_control_list_entries_cache
        else:
            data = client.get(request, "/static/control-list-entries/?flatten=True")

        for control_list_entry in data.json().get("control_list_entries", []):
            converted_control_list_entries_cache.append(
                Option(
                    key=control_list_entry["rating"],
                    value=control_list_entry["rating"],
                    description=control_list_entry["text"],
                )
            )

        return converted_control_list_entries_cache

    data = client.get(request, "/static/control-list-entries/")
    return data.json().get("control_list_entries")


# F680 clearance types
def get_f680_clearance_types(request):
    data = client.get(request, "/static/f680-clearance-types/")
    return data.json().get("types")


# Trade control activities
def get_trade_control_activities(request):
    data = client.get(request, "/static/trade-control/activities/")
    return data.json().get("activities")


# Trade control product categories
def get_trade_control_product_categories(request):
    data = client.get(request, "/static/trade-control/product-categories/")
    return data.json().get("product_categories")


# PV gradings
def get_pv_gradings(request, convert_to_options=False):
    if convert_to_options:
        data = client.get(request, "/static/private-venture-gradings/")

        converted_units = []
        for pvg in data.json().get("pv_gradings"):
            for key in pvg:
                converted_units.append(
                    Option(
                        key=key,
                        value=pvg[key],
                    )
                )
        return converted_units

    data = client.get(request, "/static/private-venture-gradings/")
    return data.json().get("pv_gradings")


def get_pv_gradings_v2(request):
    response = client.get(request, "/static/private-venture-gradings/v2/")
    response.raise_for_status()
    return response.json().get("pv_gradings")


def get_control_list_entry(request, rating):
    data = client.get(request, f"/static/control-list-entries/{rating}")
    return data.json().get("control_list_entry")


def _register_organisation(request, json, _type):
    data = {
        "type": _type,
        "user": {"email": request.session["email"]},
    }
    response = client.post(request, "/organisations/", {**json, **data})
    return response.json(), response.status_code


def register_commercial_organisation(request, json):
    return _register_organisation(request, json, "commercial")


def register_private_individual(request, json):
    return _register_organisation(request, json, "individual")


def get_open_general_licences(
    request,
    convert_to_options=False,
    name=None,
    site=None,
    status=None,
    case_type=None,
    control_list_entry=None,
    country=None,
    registered=False,
    disable_pagination=True,
    active_only=None,
):
    data = client.get(request, "/open-general-licences/" + convert_parameters_to_query_params(locals())).json()

    if convert_to_options:
        return [
            Option(
                key=ogl["id"],
                value=ogl["case_type"]["reference"]["value"] + " (" + ogl["name"] + ")",
                tag=OpenGeneralLicenceQuestions.OpenGeneralLicences.ALREADY_REGISTERED
                if ogl["registrations"]
                else None,
                more_information=ogl["description"],
                disabled=bool(len(ogl["registrations"])),
            )
            for ogl in data
        ]

    return data


def get_open_general_licence(request, pk):
    return client.get(request, f"/open-general-licences/{pk}").json()


def post_open_general_licence_cases(request, json):
    data = client.post(request, "/licences/open-general-licences/", json)
    return data.json(), data.status_code


def get_signature_certificate(request):
    certificate = client.get(request, "/documents/certificate/")
    response = HttpResponse(certificate.content, content_type=certificate.headers["Content-Type"])
    response["Content-Disposition"] = certificate.headers["Content-Disposition"]
    return response
