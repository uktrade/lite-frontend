from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_end_user_to_application(context, api_client_config):
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    lite_client.parties.add_party(context.draft_id, "end_user")
    context.end_user = lite_client.context["end_user"]
