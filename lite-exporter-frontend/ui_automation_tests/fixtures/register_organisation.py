from pytest import fixture

from shared.tools.utils import Timer, get_lite_client


@fixture(scope="session")
def register_organisation(driver, request, context, seed_data_config):
    timer = Timer()
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    context.org_registered_status = True
    context.first_name = lite_client.context["first_name"]
    context.last_name = lite_client.context["last_name"]
    context.org_name = lite_client.context["org_name"]
    context.org_id = lite_client.context["org_id"]
    timer.print_time("register_organisation")


@fixture(scope="session")
def user_details(driver, request, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    context.exporter_headers = lite_client.context["exporter_headers"]
    context.export_user_token = lite_client.context["export_user_token"]


@fixture(scope="session")
def register_organisation_for_switching_organisation(driver, request, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_org.setup_org_for_switching_organisations()
    context.org_name_for_switching_organisations = lite_client.context["org_name_for_switching_organisations"]
