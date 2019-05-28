from conf.client import get, post
from conf.constants import UNITS_URL, DRAFTS_URL
from libraries.forms.components import Option


def get_units(request):
    data = get(request, UNITS_URL).json()
    converted_units = []

    for key, value in data.get('units').items():
        converted_units.append(
           Option(key, value)
        )

    return converted_units


def get_sites_on_draft(request, pk):
    data = get(request, DRAFTS_URL + pk + '/sites/')
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/sites/', json)
    return data.json(), data.status_code
