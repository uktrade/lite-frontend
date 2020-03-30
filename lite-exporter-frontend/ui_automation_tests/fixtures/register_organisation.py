from pytest import fixture

from ui_automation_tests.shared.tools.utils import Timer


@fixture(scope="session")
def register_organisation(context, api_test_client):
    timer = Timer()
    context.org_registered_status = True
    context.first_name = api_test_client.context["first_name"]
    context.last_name = api_test_client.context["last_name"]
    context.org_name = api_test_client.context["org_name"]
    context.org_id = api_test_client.context["org_id"]
    timer.print_time("register_organisation")


@fixture(scope="session")
def register_organisation_for_switching_organisation(context, api_test_client):
    api_test_client.organisations.setup_org_for_switching_organisations()
    context.org_name_for_switching_organisations = api_test_client.context["org_name_for_switching_organisations"]
