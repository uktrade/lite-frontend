from conf.client import get, post, put
from conf.constants import SITES_URL, ORGANISATIONS_URL, NEWLINE, USERS_URL
from core.helpers import convert_value_to_query_param
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Option


def get_sites(request, organisation_id, convert_to_options=False, exclude: list = None):
    data = get(
        request,
        ORGANISATIONS_URL + str(organisation_id) + SITES_URL + "?" + convert_value_to_query_param("exclude", exclude),
    ).json()["sites"]

    primary_site = " " + strings.sites.SitesPage.PRIMARY_SITE

    if convert_to_options:
        sites_options = []

        for site in data:
            if primary_site:
                primary_site = ""

            site_id = site.get("id")
            site_name = site.get("name") + primary_site
            address = site.get("address")

            site_address = NEWLINE.join(
                filter(
                    None,
                    [
                        address.get("address_line_1"),
                        address.get("address_line_2"),
                        address.get("postcode"),
                        address.get("city"),
                        address.get("country").get("name"),
                    ],
                )
            )

            sites_options.append(Option(site_id, site_name, description=site_address))

        return sites_options

    return data


def get_site(request, organisation_id, pk):
    data = get(request, ORGANISATIONS_URL + str(organisation_id) + SITES_URL + str(pk))
    return data.json()["site"]


def put_site(request, organisation_id, pk, json):
    data = put(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk + "/", json=json)
    return data.json(), data.status_code


def post_sites(request, organisation_id, json):
    data = post(request, ORGANISATIONS_URL + organisation_id + SITES_URL, json)
    return data.json(), data.status_code


def put_assign_sites(request, pk, json):
    data = put(request, USERS_URL + str(pk) + SITES_URL, json)
    return data.json(), data.status_code
