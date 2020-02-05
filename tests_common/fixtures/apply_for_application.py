import datetime

from pytest import fixture

from ..tools.utils import get_lite_client, Timer


def save_application_data_to_context(lite_client, context):
    context.app_id = lite_client.context["application_id"]
    context.case_id = lite_client.context["application_id"]
    context.end_user = lite_client.context["end_user"]
    context.consignee = lite_client.context["consignee"]
    context.third_party = lite_client.context["third_party"]
    context.ultimate_end_user = lite_client.context["ultimate_end_user"]


def generate_name(prefix):
    time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    return f"{prefix}{time_id}", time_id


@fixture
def apply_for_standard_application(driver, seed_data_config, context):
    timer = Timer()
    lite_client = get_lite_client(context, seed_data_config)

    context.app_name, context.app_time_id = generate_name("Standard Application")
    context.good_value = 1.21

    draft_id = lite_client.add_draft(
        draft={
            "name": context.app_name,
            "application_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
        },
        good={
            "good_id": "",
            "quantity": 1234,
            "unit": "MTR",
            "value": context.good_value,
            "is_good_incorporated": True,
            "is_good_pv_graded": "no",
        },
        end_user={
            "name": "Mr Smith",
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk",
        },
        ultimate_end_user={
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "sub_type": "commercial",
            "website": "https://www.anothergov.uk",
        },
        consignee={
            "name": "Government",
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk",
        },
        third_party={
            "name": "Individual",
            "address": "Ukraine, 01532",
            "country": "UA",
            "sub_type": "government",
            "role": "agent",
            "website": "https://www.anothergov.uk",
        },
    )
    lite_client.submit_standard_application(draft_id)
    save_application_data_to_context(lite_client, context)
    timer.print_time("apply_for_standard_application")


@fixture(scope="module")
def add_an_ecju_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_ecju.add_ecju_query(context.case_id)


@fixture(scope="function")
def apply_for_clc_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_clc.add_goods_query(lite_client.seed_good)
    context.clc_case_id = lite_client.context["case_id"]


@fixture(scope="function")
def apply_for_grading_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_grading.add_goods_query(lite_client.seed_good)
    context.clc_case_id = lite_client.context["case_id"]


# The below is currently not used due to bug LT-1808 but willl need to be used for internal HMRC tests when fixed.
@fixture(scope="function")
def apply_for_hmrc_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_user.auth_export_user(lite_client.context["hmrc_org_id"])

    draft_id = lite_client.add_hmrc_draft(
        draft={
            "application_type": "hmrc_query",
            "organisation": lite_client.context["org_id"],
            "hmrc_organisation": lite_client.context["hmrc_org_id"],
        },
        good={"good_id": "", "quantity": 1234, "unit": "MTR", "value": 1, "is_good_incorporated": True},
        end_user={
            "name": "Mr Smith",
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk",
        },
    )
    lite_client.submit_hmrc_application(draft_id)


@fixture(scope="module")
def apply_for_eua_query(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_party.add_eua_query()
    context.eua_id = lite_client.context["end_user_advisory_id"]
    context.eua_reference_code = lite_client.context["end_user_advisory_reference_code"]


@fixture(scope="module")
def apply_for_open_application(driver, seed_data_config, context):
    timer = Timer()
    lite_client = get_lite_client(context, seed_data_config)

    context.open_app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_name = "Test Application " + context.open_app_time_id

    draft_id = lite_client.add_open_draft(
        draft={
            "name": context.app_name,
            "application_type": "open_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
        }
    )
    lite_client.submit_open_application(draft_id)
    context.app_id = lite_client.context["application_id"]
    context.case_id = lite_client.context["application_id"]
    context.country = lite_client.context["country"]
    timer.print_time("apply_for_open_application")


@fixture(scope="module")
def apply_for_exhibition_clearance(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    context.app_name, context.app_time_id = generate_name("Exhibition Clearance")
    draft_id = lite_client.add_draft(draft={"name": context.app_name, "application_type": "exhibition_clearance",})
    lite_client.submit_exhibition_application(draft_id)
    save_application_data_to_context(lite_client, context)
    context.reference_code = lite_client.context["reference_code"]
