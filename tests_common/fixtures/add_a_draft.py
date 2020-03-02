from pytest import fixture

from ui_automation_tests.shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_a_draft(context, api_client_config):
    context.draft_id = get_lite_client(context, api_client_config).applications.create_draft()
