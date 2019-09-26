from pytest import fixture
import datetime
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="module")
def apply_for_standard_application(driver, request, api_url, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))

    app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_time_id = app_time_id

    api.add_draft(
        draft={
            "name": "Test Application " + app_time_id,
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
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk"
        },
        ultimate_end_user={
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "sub_type": "commercial",
            "website": "https://www.anothergov.uk"
        },
        consignee={
            "name": "Government",
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk"
        },
        third_party={
            "name": "Individual",
            "address": "Ukraine, 01532",
            "country": "UA",
            "sub_type": "agent",
            "website": "https://www.anothergov.uk"
        }

    )
    api.submit_application()
    context.app_id = api.context['application_id']
    context.case_id = api.context['case_id']
    context.end_user = api.context['end_user']
    context.consignee = api.context['consignee']
    context.third_party = api.context['third_party']
    context.ultimate_end_user = api.context['ultimate_end_user']

    timer.print_time('apply_for_standard_application')


@fixture(scope="module")
def apply_for_clc_query(driver, request, api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_clc_query()
    context.clc_case_id = api.context['case_id']


@fixture(scope="module")
def apply_for_eua_query(driver, request, api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_eua_query()
    context.eua_id = api.context['end_user_advisory_id']
