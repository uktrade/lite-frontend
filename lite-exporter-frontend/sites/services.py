from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import SITES_URL, ORGANISATIONS_URL
from core.services import get_organisation


def get_sites(request, organisation_id, formatted=False):
    organisation = get_organisation(request, str(organisation_id))
    data = get(request, ORGANISATIONS_URL + str(organisation_id) + SITES_URL)

    if formatted:
        sites_options = []

        for site in data.json().get('sites'):
            primary_site = '(Primary Site)' if site.get('id') == organisation['primary_site']['id'] else ''
            site_id = site.get('id')
            site_name = site.get('name') + ' ' + primary_site
            address = site.get('address')

            site_address = '\n'.join(filter(None, [address.get('address_line_1'),
                                                   address.get('address_line_2'),
                                                   address.get('postcode'),
                                                   address.get('city')]))

            sites_options.append(
                Option(site_id, site_name, description=site_address)
            )

        return sites_options

    return data.json(), data.status_code


def get_site(request, organisation_id, pk):
    data = get(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk)
    return data.json(), data.status_code


def put_site(request, organisation_id, pk, json):
    data = put(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk + '/', json=json)
    return data.json(), data.status_code


def post_sites(request, organisation_id, json):
    data = post(request, ORGANISATIONS_URL + organisation_id + SITES_URL, json)
    return data.json(), data.status_code
