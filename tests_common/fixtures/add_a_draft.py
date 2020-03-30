from pytest import fixture


@fixture(scope="function")
def add_a_draft(context, api_test_client):
    context.draft_id = api_test_client.applications.create_draft()
