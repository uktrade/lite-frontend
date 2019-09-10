from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import UNITS_URL, DRAFTS_URL, COUNTRIES_URL, EXTERNAL_LOCATIONS_URL, NOTIFICATIONS_URL, \
    CLC_NOTIFICATIONS_URL, ORGANISATIONS_URL


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
                Option(country.get('id'), country.get('name'))
            )

        return converted_units

    return data.json(), data.status_code


def get_sites_on_draft(request, pk):
    data = get(request, DRAFTS_URL + pk + '/sites/')
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/sites/', json)
    return data.json(), data.status_code


def get_external_locations(request, pk, formatted=False):
    data = get(request, ORGANISATIONS_URL + str(pk) + EXTERNAL_LOCATIONS_URL)

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
    data = get(request, DRAFTS_URL + pk + '/external_locations/')
    return data.json(), data.status_code


def post_external_locations_on_draft(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/external_locations/', json)
    return data.json(), data.status_code


def post_external_locations(request, pk, json):
    data = post(request, ORGANISATIONS_URL + pk + EXTERNAL_LOCATIONS_URL, json)
    return data.json(), data.status_code


def get_notifications(request, unviewed):
    url = NOTIFICATIONS_URL
    if unviewed:
        url = '%s?unviewed=True' % url
    data = get(request, url)
    return data.json(), data.status_code


def get_clc_notifications(request, unviewed):
    url = CLC_NOTIFICATIONS_URL
    if unviewed:
        url = '%s?unviewed=True' % url
    data = get(request, url)
    return data.json(), data.status_code


# Organisation
def get_organisation(request, pk):
    data = get(request, ORGANISATIONS_URL + pk)
    return data.json()['organisation'], data.status_code


def get_organisation_users(request, pk):
    data = get(request, ORGANISATIONS_URL + pk + '/users/')
    return data.json(), data.status_code


def get_organisation_user(request, pk, user_pk):
    data = get(request, ORGANISATIONS_URL + pk + '/users/' + user_pk)
    return data.json()


def put_organisation_user(request, pk, user_pk, json):
    data = put(request, ORGANISATIONS_URL + pk + '/users/' + user_pk + '/', json)
    return data.json(), data.status_code
