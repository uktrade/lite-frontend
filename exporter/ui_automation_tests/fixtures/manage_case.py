from http import HTTPStatus

from pytest import fixture


@fixture(scope="function")
def manage_case_status_to_withdrawn(api_test_client, context):
    status = api_test_client.cases.manage_case_status(context.app_id, "withdrawn")
    assert status == HTTPStatus.OK, "Case status not updated to new status"


@fixture(scope="function")
def approve_case(api_test_client, context):
    status = api_test_client.cases.finalise_case(context.app_id, "approve")
    assert status == HTTPStatus.OK, "Case cannot be finalised"
