from pytest_bdd import then, scenarios, given

from shared.tools.utils import get_lite_client
from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/copied_application.feature", strict_gherkin=False)


@then("I can see the original application is linked")
def original_application_linked(driver, context):
    assert context.old_app_id in ApplicationPage(driver).get_case_copy_of_field_href()


@given("I have an open application from copying")  # noqa
def copy_open_app(driver, apply_for_open_application, api_client_config, context):  # noqa
    lite_client = get_lite_client(context, api_client_config)  # noqa
    app_name = {"name": "new application"}
    end_use_details = {
        "intended_end_use": "intended end use",
        "is_military_end_use_controls": False,
        "is_informed_wmd": False,
        "is_suspected_wmd": False,
    }
    route_of_goods = {"is_shipped_waybill_or_lading": True}

    lite_client.applications.add_copied_open_application(context.app_id, app_name, end_use_details, route_of_goods)
    context.old_app_id = context.app_id
    context.app_id = lite_client.context["application_id"]
    context.case_id = lite_client.context["application_id"]
    context.reference_code = lite_client.context["reference_code"]
