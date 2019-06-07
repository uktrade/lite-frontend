from conf.client import get, post
from conf.constants import UNITS_URL, DRAFTS_URL, COUNTRIES_URL, EXTERNAL_LOCATIONS_URL
from libraries.forms.components import Option


def get_units(request):
    data = get(request, UNITS_URL).json()
    converted_units = []

    for key, value in data.get('units').items():
        converted_units.append(
           Option(key, value)
        )

    return converted_units


def get_countries(request, convert_to_options=False):
    data = get(request, COUNTRIES_URL)

    if convert_to_options:
        converted_units = []

        for country in data.json().get('countries'):
            converted_units.append(
                Option(country.get('name'), country.get('name'))
            )

        return converted_units

    return data.json(), data.status_code


def get_sites_on_draft(request, pk):
    data = get(request, DRAFTS_URL + pk + '/sites/')
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/sites/', json)
    return data.json(), data.status_code


def get_external_locations(request, formatted=False):
    data = get(request, EXTERNAL_LOCATIONS_URL)

    if formatted:
        external_locations_options = []

        for external_location in data.json().get('external_locations'):
            external_location_id = external_location.get('id')
            external_location_name = external_location.get('name')
            external_location_address = external_location.get('address')


            external_locations_options.append(
                Option(external_location_id, external_location_name, description=external_location_address)
            )

        return external_locations_options

    return data.json(), data.status_code


def get_external_locations_on_draft(request, pk):
    data = get(request, DRAFTS_URL + pk + '/external_locations')
    return data.json(), data.status_code


def post_external_locations_on_draft(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/external_locations', json)
    return data.json(), data.status_code


def post_external_locations(request, json):
    data = post(request, EXTERNAL_LOCATIONS_URL, json)
    return data.json(), data.status_code
