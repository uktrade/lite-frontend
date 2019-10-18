import datetime

from pytest import fixture

from ..tools.utils import Timer, get_lite_client


@fixture(scope="module")
def apply_for_standard_application(driver, seed_data_config, context):
    timer = Timer()
    lite_client = get_lite_client(context, seed_data_config)

    app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_time_id = app_time_id
    app_name = "Test Application" + app_time_id

    lite_client.add_draft(
        draft={
            "name": app_name,
            "licence_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"
        },
        good={
            "good_id": "",
            "quantity": 1234,
            "unit": "MTR",
            "value": 1
        },
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
    lite_client.submit_standard_application()
    context.app_id = lite_client.context['application_id']
    context.case_id = lite_client.context['case_id']
    context.end_user = lite_client.context['end_user']
    context.consignee = lite_client.context['consignee']
    context.third_party = lite_client.context['third_party']
    context.ultimate_end_user = lite_client.context['ultimate_end_user']
    context.app_name = app_name
    timer.print_time('apply_for_standard_application')


@fixture(scope="module")
def add_an_ecju_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_ecju.add_ecju_query(context.case_id)


@fixture(scope="module")
def apply_for_clc_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_clc.add_clc_query(lite_client.seed_good)
    context.clc_case_id = lite_client.context['case_id']


@fixture(scope="module")
def apply_for_eua_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_party.add_eua_query()
    context.eua_id = lite_client.context['end_user_advisory_id']


@fixture(scope="module")
def apply_for_open_application(driver, seed_data_config, context):
    timer = Timer()
    lite_client = get_lite_client(context, seed_data_config)

    context.open_app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_name = "Test Application " + context.open_app_time_id

    lite_client.add_open_draft(
        draft={
            "name": context.app_name,
            "licence_type": "open_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"}
    )
    lite_client.submit_open_application()
    context.app_id = lite_client.context['application_id']
    context.case_id = lite_client.context['case_id']
    context.country = lite_client.context['country']
    timer.print_time('apply_for_open_application')
