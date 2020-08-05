from pytest import fixture


@fixture(scope="module")
def add_end_user_advisory(context, api_test_client):
    api_test_client.parties.add_eua_query()
    context.end_user_advisory_id = api_test_client.context["end_user_advisory_id"]
    context.end_user_advisory_name = api_test_client.context["end_user_advisory_name"]
