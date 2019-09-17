from conf.client import get, post
from conf.constants import ORGANISATIONS_URL, SITES_URL


def get_organisations(request):
    data = get(request, ORGANISATIONS_URL)
    return data.json(), data.status_code


def post_organisations(request, json):
    data = post(request, ORGANISATIONS_URL, json)
    return data.json(), data.status_code


def get_organisations_sites(request, pk):
    data = get(request, ORGANISATIONS_URL + pk + SITES_URL)
    return data.json(), data.status_code


def get_organisation(request, pk):
    data = get(request, ORGANISATIONS_URL + pk)
    return data.json(), data.status_code
