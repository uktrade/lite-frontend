from pytest import fixture

from ui_automation_tests.shared.tools.utils import get_lite_client


@fixture(scope="function")
def manage_case_status_to_withdrawn(driver, api_client_config, context):
    lite_client = get_lite_client(context, api_client_config)
    status = lite_client.cases.manage_case_status(context.app_id, "withdrawn")
    assert status == 200, "Case status not updated to new status"


@fixture(scope="function")
def approve_case(driver, api_client_config, context):
    lite_client = get_lite_client(context, api_client_config)
    status = lite_client.cases.finalise_case(context.app_id, "approve")
    assert status == 200, "Case cannot be finalised"
