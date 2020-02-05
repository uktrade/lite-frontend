from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture
def manage_case_status_to_withdrawn(driver, api_client_config, context):
    lite_client = get_lite_client(context, api_client_config)
    status = lite_client.manage_case_status(context.app_id)
    assert status == 200, "Case status not updated to new status"
