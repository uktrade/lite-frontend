from pytest import fixture
from faker import Faker

fake = Faker()

from ..tools.utils import Timer


def save_application_data_to_context(lite_client, context):
    context.app_id = lite_client.context["application_id"]
    context.case_id = lite_client.context["application_id"]
    context.reference_code = lite_client.context["reference_code"]
    context.end_user = lite_client.context.get("end_user")
    context.consignee = lite_client.context.get("consignee")
    context.third_party = lite_client.context.get("third_party")
    context.ultimate_end_user = lite_client.context.get("ultimate_end_user")


@fixture(scope="function")
def apply_for_standard_application(api_test_client, context):
    timer = Timer()
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    context.app_name = fake.bs()
    context.good_value = 1.21

    draft_id = api_test_client.applications.add_draft(
        draft={
            "name": context.app_name,
            "application_type": "siel",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
            "contains_firearm_goods": True,
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
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "end_user",
        },
        ultimate_end_user={
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "GB",
            "sub_type": "commercial",
            "website": fake.uri(),
            "type": "ultimate_end_user",
        },
        consignee={
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "consignee",
        },
        third_party={
            "name": fake.name(),
            "address": fake.street_address() + ", " + fake.state() + ", " + fake.postcode(),
            "country": "UA",
            "sub_type": "government",
            "role": "agent",
            "website": fake.uri(),
            "type": "third_party",
        },
        end_use_details={
            "intended_end_use": "intended end use",
            "is_military_end_use_controls": False,
            "is_informed_wmd": False,
            "is_suspected_wmd": False,
            "is_eu_military": False,
        },
        route_of_goods={"is_shipped_waybill_or_lading": True},
    )
    data = api_test_client.applications.submit_application(draft_id)
    save_application_data_to_context(api_test_client, context)
    context.good_id = api_test_client.context.get("good_id")
    context.goods = data["application"]["goods"]
    timer.print_time("apply_for_standard_application")


@fixture(scope="module")
def add_an_ecju_query(api_test_client, context):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    api_test_client.ecju_queries.add_ecju_query(context.case_id)


@fixture(scope="function")
def apply_for_clc_query(api_test_client, context):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    api_test_client.goods_queries.add_goods_clc_query(api_test_client.goods)
    context.clc_case_id = api_test_client.context["case_id"]


@fixture(scope="function")
def apply_for_grading_query(api_test_client, context):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    api_test_client.goods_queries.add_goods_grading_query(api_test_client.goods)
    context.clc_case_id = api_test_client.context["case_id"]


# The below is currently not used due to bug LT-1808 but willl need to be used for internal HMRC tests when fixed.
@fixture(scope="function")
def apply_for_hmrc_query(api_test_client, context):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["hmrc_org_id"])
    draft_id = api_test_client.applications.add_hmrc_draft(
        draft={
            "application_type": "cre",
            "organisation": api_test_client.context["org_id"],
            "hmrc_organisation": api_test_client.context["hmrc_org_id"],
        },
        end_user={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "end_user",
        },
    )
    api_test_client.applications.submit_application(draft_id, is_hmrc=True)
    context.case_id = api_test_client.context["case_id"]
    context.reference_code = api_test_client.context["reference_code"]


@fixture(scope="module")
def apply_for_eua_query(driver, api_test_client, context):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    api_test_client.parties.add_eua_query()
    context.eua_id = api_test_client.context["end_user_advisory_id"]
    context.eua_reference_code = api_test_client.context["end_user_advisory_reference_code"]


@fixture(scope="module")
def apply_for_open_application(api_test_client, context):
    timer = Timer()
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])

    context.app_name = fake.bs()

    draft_id = api_test_client.applications.add_open_draft(
        draft={
            "name": context.app_name,
            "application_type": "oiel",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
            "goodstype_category": "military",
            "contains_firearm_goods": True,
        },
        end_use_details={
            "intended_end_use": "intended end use",
            "is_military_end_use_controls": False,
            "is_informed_wmd": False,
            "is_suspected_wmd": False,
        },
        ultimate_end_user={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "commercial",
            "website": fake.uri(),
            "type": "ultimate_end_user",
        },
        route_of_goods={"is_shipped_waybill_or_lading": True},
    )
    data = api_test_client.applications.submit_application(draft_id)
    save_application_data_to_context(api_test_client, context)
    context.country = api_test_client.context["country"]
    context.goods_type = data["application"]["goods_types"][0]
    timer.print_time("apply_for_open_application")


def _apply_for_mod_clearance(
    type, has_end_user, has_consignee, has_ultimate_end_user, has_third_party, has_location, api_test_client, context
):
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    context.app_name = fake.bs()

    draft_id = api_test_client.applications.add_draft(
        draft={
            "name": context.app_name,
            "application_type": type,
            "clearance_level": "uk_official" if type == "f680" else None,
        },
        end_user={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "end_user",
            "clearance_level": "uk_official" if type == "f680" else None,
        },
        ultimate_end_user={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "commercial",
            "website": fake.uri(),
            "type": "ultimate_end_user",
            "clearance_level": "uk_official" if type == "f680" else None,
        },
        consignee={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "consignee",
            "clearance_level": "uk_official" if type == "f680" else None,
        },
        third_party={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "UA",
            "sub_type": "government",
            "role": "agent",
            "website": fake.uri(),
            "type": "third_party",
            "clearance_level": "uk_official" if type == "f680" else None,
        },
        has_end_user=has_end_user,
        has_consignee=has_consignee,
        has_ultimate_end_user=has_ultimate_end_user,
        has_third_party=has_third_party,
        has_location=has_location,
        f680_clearance_types=["market_survey"] if type == "f680" else None,
        additional_information={
            "expedited": False,
            "mtcr_type": "mtcr_category_2",
            "foreign_technology": False,
            "locally_manufactured": False,
            "uk_service_equipment": False,
            "uk_service_equipment_type": "mod_funded",
            "electronic_warfare_requirement": False,
            "prospect_value": 100.0,
        }
        if type == "f680"
        else None,
        end_use_details={"intended_end_use": "intended end use"} if type == "f680" else None,
    )
    if type == "exhc":
        api_test_client.applications.post_exhibition_details(draft_id=draft_id, data=None)
    data = api_test_client.applications.submit_application(draft_id)
    save_application_data_to_context(api_test_client, context)
    context.goods = data["application"]["goods"]


@fixture(scope="module")
def apply_for_exhibition_clearance(driver, api_test_client, context):
    _apply_for_mod_clearance(
        type="exhc",
        has_consignee=False,
        has_ultimate_end_user=False,
        has_end_user=False,
        has_third_party=False,
        has_location=False,
        api_test_client=api_test_client,
        context=context,
    )


@fixture(scope="module")
def apply_for_f680_clearance(driver, api_test_client, context):
    _apply_for_mod_clearance(
        type="f680",
        has_end_user=True,
        has_third_party=True,
        has_consignee=False,
        has_ultimate_end_user=False,
        has_location=False,
        api_test_client=api_test_client,
        context=context,
    )


@fixture(scope="module")
def apply_for_gifting_clearance(driver, api_test_client, context):
    _apply_for_mod_clearance(
        type="gift",
        has_end_user=True,
        has_third_party=True,
        has_consignee=False,
        has_ultimate_end_user=False,
        has_location=False,
        api_test_client=api_test_client,
        context=context,
    )


@fixture
def apply_for_trade_control_application(api_test_client, context):
    timer = Timer()
    api_test_client.api_client.auth_exporter_user(api_test_client.context["org_id"])
    context.app_name = fake.bs()
    context.good_value = 1.21

    draft_id = api_test_client.applications.add_draft(
        draft={
            "name": context.app_name,
            "application_type": "sicl",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234",
            "trade_control_activity": "transfer_of_goods",
            "trade_control_product_categories": ["category_a"],
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
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "end_user",
        },
        ultimate_end_user={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "commercial",
            "website": fake.uri(),
            "type": "ultimate_end_user",
        },
        consignee={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "GB",
            "sub_type": "government",
            "website": fake.uri(),
            "type": "consignee",
        },
        third_party={
            "name": fake.name(),
            "address": fake.street_address() + fake.state() + fake.postcode(),
            "country": "UA",
            "sub_type": "government",
            "role": "agent",
            "website": fake.uri(),
            "type": "third_party",
        },
        end_use_details={
            "intended_end_use": "intended end use",
            "is_military_end_use_controls": False,
            "is_informed_wmd": False,
            "is_suspected_wmd": False,
            "is_eu_military": False,
        },
        route_of_goods={"is_shipped_waybill_or_lading": True},
        external_location={
            "name": fake.name(),
            "address": fake.street_address(),
            "country": "FR",
            "location_type": "land_based",
            "application_type": "sicl",
        },
        has_location=False,
        has_external_location=True,
    )
    data = api_test_client.applications.submit_application(draft_id)
    save_application_data_to_context(api_test_client, context)
    context.good_id = api_test_client.context.get("good_id")
    context.goods = data["application"]["goods"]
    timer.print_time("apply_for_standard_application")
