from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import UNITS_URL, DRAFTS_URL, COUNTRIES_URL, EXTERNAL_LOCATIONS_URL, NOTIFICATIONS_URL, \
    ORGANISATIONS_URL, CASES_URL, CONTROL_LIST_ENTRIES_URL


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
    return data.json()['results']


# Organisation
def get_organisation(request, pk):
    data = get(request, ORGANISATIONS_URL + pk)
    return data.json()


def get_organisation_users(request, pk):
    data = get(request, ORGANISATIONS_URL + pk + '/users/')
    return data.json(), data.status_code


def get_organisation_user(request, pk, user_pk):
    data = get(request, ORGANISATIONS_URL + pk + '/users/' + user_pk)
    return data.json()


def put_organisation_user(request, pk, user_pk, json):
    data = put(request, ORGANISATIONS_URL + pk + '/users/' + user_pk + '/', json)
    return data.json(), data.status_code


# Cases
def get_case(request, pk):
    data = get(request, CASES_URL + pk)
    return data.json()['case']


# Control List Entries
def get_control_list_entries(request, convert_to_options=False):
    if convert_to_options:
        data = get(request, CONTROL_LIST_ENTRIES_URL + '?flatten=True')

        converted_units = []

        for control_list_entry in data.json()['control_list_entries']:
            converted_units.append(Option(key=control_list_entry['rating'],
                                          value=control_list_entry['rating'],
                                          description=control_list_entry['text']))

        return converted_units

    data = get(request, CONTROL_LIST_ENTRIES_URL)
    return data.json()['control_list_entries']
