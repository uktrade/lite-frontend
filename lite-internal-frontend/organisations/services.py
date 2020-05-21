from http import HTTPStatus

from conf.client import get, post, put
from conf.constants import ORGANISATIONS_URL, SITES_URL, USERS_URL, ORGANISATION_STATUS_URL, ACTIVITY_URL
from lite_content.lite_internal_frontend.organisations import RegisterAnOrganisation


def get_organisations(request, params):
    data = get(request, ORGANISATIONS_URL + "?" + params)
    return data.json(), data.status_code


def post_organisations(request, json):
    errors = {}

    if not json.get("type"):
        errors["type"] = [RegisterAnOrganisation.CommercialOrIndividual.ERROR]

    if not json.get("location"):
        errors["location"] = [RegisterAnOrganisation.WhereIsTheExporterBased.ERROR]

    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    data = post(request, ORGANISATIONS_URL, json)
    return data.json(), data.status_code


def post_hmrc_organisations(request, json):
    data = post(request, ORGANISATIONS_URL, json)
    return data.json(), data.status_code


def put_organisation(request, pk, json):
    if "status" in json:
        del json["status"]
    data = put(request, ORGANISATIONS_URL + str(pk) + "/", json)
    return data.json(), data.status_code


def put_organisation_status(request, pk, json):
    data = put(request, ORGANISATIONS_URL + str(pk) + ORGANISATION_STATUS_URL, json)
    return data.json(), data.status_code


def get_organisation(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk))
    return data.json()


def get_organisation_sites(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk) + SITES_URL + "?disable_pagination=True")
    return data.json()["sites"]


def get_organisation_members(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk) + USERS_URL + "?disable_pagination=True")
    return data.json()


def get_organisation_matching_details(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk) + "/matching_details/")
    return data.json()["matching_properties"]


def get_organisation_activity(request, pk):
    url = ORGANISATIONS_URL + str(pk) + ACTIVITY_URL
    data = get(request, url)
    return data.json()["activity"]
