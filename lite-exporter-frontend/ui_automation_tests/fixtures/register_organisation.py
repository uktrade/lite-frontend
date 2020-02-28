from pytest import fixture

from ui_automation_tests.shared.tools.utils import Timer, get_lite_client


@fixture(scope="session")
def register_organisation(context, api_client_config):
    timer = Timer()
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    context.org_registered_status = True
    context.first_name = lite_client.context["first_name"]
    context.last_name = lite_client.context["last_name"]
    context.org_name = lite_client.context["org_name"]
    context.org_id = lite_client.context["org_id"]
    timer.print_time("register_organisation")


@fixture(scope="session")
def register_organisation_for_switching_organisation(context, api_client_config):
    lite_client = get_lite_client(context, api_client_config=api_client_config)
    lite_client.organisations.setup_org_for_switching_organisations()
    context.org_name_for_switching_organisations = lite_client.context["org_name_for_switching_organisations"]
