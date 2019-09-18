from pytest import fixture
import datetime

from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="module")
def add_an_application(driver, request, api_url, exporter_url, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))

    app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_time_id = app_time_id
    app_name = "Test Application" + app_time_id

    api.add_draft(
        draft={
            "name": app_name,
            "licence_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"},
        good={
            "good_id": "",
            "quantity": 1234,
            "unit": "MTR",
            "value": 1},
        enduser={
            "name": "Mr Smith",
            "address": "London",
            "country": "UA",
            "sub_type": "government",
            "website": "https://www.smith.com"
        },
        ultimate_end_user={
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "sub_type": "commercial",
            "website": "https://www.anothergov.uk"
        },
        consignee={
             'name': 'Government',
             'address': 'Westminster, London SW1A 0BB',
             'country': 'GB',
             'sub_type': 'government',
             'website': 'https://www.gov.uk'
        }
    )
    api.submit_application()
    context.app_id = api.context['application_id']
    context.app_name = app_name
    context.case_id = api.context['case_id']
    api.add_ecju_query(context.case_id)
    timer.print_time('apply_for_standard_application')