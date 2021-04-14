from http import HTTPStatus
from lite_forms.helpers import nest_data

from core import client
from lite_content.lite_internal_frontend.organisations import RegisterAnOrganisation


def get_organisations(request, params):
    data = client.get(request, f"/organisations/?{params}")
    return data.json(), data.status_code


def post_organisations(request, json):
    errors = {}

    if not json.get("type"):
        errors["type"] = [RegisterAnOrganisation.CommercialOrIndividual.ERROR]

    if not json.get("location"):
        errors["location"] = [RegisterAnOrganisation.WhereIsTheExporterBased.ERROR]

    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    data = client.post(request, "/organisations/", json)
    return data.json(), data.status_code


def post_hmrc_organisations(request, json):
    data = client.post(request, "/organisations/", json)
    return data.json(), data.status_code


def put_organisation(request, pk, json):
    if "status" in json:
        del json["status"]

    json = nest_data(json)
    data = client.put(request, f"/organisations/{pk}/", json)
    return data.json(), data.status_code


def put_organisation_status(request, pk, json):
    data = client.put(request, f"/organisations/{pk}/status/", json)
    return data.json(), data.status_code


def get_organisation(request, pk):
    data = client.get(request, f"/organisations/{pk}")
    return data.json()


def get_organisation_sites(request, pk):
    data = client.get(request, f"/organisations/{pk}/sites/?disable_pagination=True")
    return data.json()["sites"]


def get_organisation_members(request, pk):
    data = client.get(request, f"/organisations/{pk}/users/?disable_pagination=True")
    return data.json()


def get_organisation_matching_details(request, pk):
    data = client.get(request, f"/organisations/{pk}/matching_details/")
    return data.json()["matching_properties"]


def get_organisation_activity(request, pk):
    url = f"/organisations/{pk}/activity/"
    data = client.get(request, url)
    return data.json()["activity"]


def get_site_activity(request, pk):
    url = f"/organisations/{pk}/sites-activity/"
    data = client.get(request, url)
    return data.json()["activity"]
