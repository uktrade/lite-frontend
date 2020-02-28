from pytest import fixture

from ui_automation_tests.shared.tools.utils import get_lite_client


@fixture(scope="module")
def add_end_user_advisory(context, api_client_config):
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    lite_client.parties.add_eua_query()
    context.end_user_advisory_id = lite_client.context["end_user_advisory_id"]
