from http import HTTPStatus

from core import client
from core.helpers import convert_value_to_query_param
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.sites import AddSiteForm
from lite_forms.components import Option


def get_sites(
    request, organisation_id, convert_to_options=False, get_total_users=False, exclude: list = None, postcode=None
):
    querystring = "&".join(
        [
            convert_value_to_query_param("exclude", exclude),
            convert_value_to_query_param("get_total_users", get_total_users),
            convert_value_to_query_param("postcode", postcode),
        ]
    )
    data = client.get(request, f"/organisations/{organisation_id}/sites/?{querystring}").json()["sites"]

    primary_site = " " + strings.sites.SitesPage.PRIMARY_SITE

    if convert_to_options:
        sites_options = []

        for site in data:
            if primary_site:
                primary_site = ""

            site_id = site.get("id")
            site_name = site.get("name") + primary_site
            address = site.get("address")

            site_address = "\n".join(
                filter(
                    None,
                    [
                        address.get("address"),
                        address.get("address_line_1"),
                        address.get("address_line_2"),
                        address.get("city"),
                        address.get("postcode"),
                        address.get("country").get("name"),
                    ],
                )
            )

            sites_options.append(Option(site_id, site_name, description=site_address))

        return sites_options

    return data


def filter_sites_in_the_uk(sites):
    uk_sites = []
    for site in sites:
        if site["address"]["country"]["id"] == "GB":
            uk_sites.append(site)
    return uk_sites


def get_site(request, organisation_id, pk):
    data = client.get(request, f"/organisations/{organisation_id}/sites/{pk}")
    return data.json()


def update_site(request, pk, json):
    organisation_id = request.session["organisation"]
    response = client.patch(request, f"/organisations/{organisation_id}/sites/{pk}/", data=json,)
    return response.json(), response.status_code


def post_sites(request, organisation_id, json):
    if json.get("are_you_sure", True) == "None":
        return (
            {"errors": {"are_you_sure": [AddSiteForm.WhereIsYourSiteBased.EXISTING_SITE_ERROR]}},
            HTTPStatus.BAD_REQUEST,
        )

    if "location" not in json:
        return {"errors": {"location": [AddSiteForm.WhereIsYourSiteBased.ERROR]}}, HTTPStatus.BAD_REQUEST

    data = client.post(request, f"/organisations/{organisation_id}/sites/", json)
    return data.json(), data.status_code


def put_assign_sites(request, pk, json):
    data = client.put(request, f"/users/{pk}/sites/", json)
    return data.json(), data.status_code
