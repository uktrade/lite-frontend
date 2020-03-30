from pytest import fixture


@fixture(scope="function")
def add_end_user_to_application(context, api_test_client):
    api_test_client.parties.add_party(context.draft_id, "end_user")
    context.end_user = api_test_client.context["end_user"]
