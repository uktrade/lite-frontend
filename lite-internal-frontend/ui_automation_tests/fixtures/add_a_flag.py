from pytest import fixture
import shared.tools.helpers as utils


@fixture(scope="function")
def add_case_flag(context, api_test_client):
    api_test_client.flags.add_flag("Case " + utils.get_formatted_date_time_m_d_h_s(), "Case")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="function")
def add_good_flag(context, api_test_client):
    api_test_client.flags.add_flag("Good " + utils.get_formatted_date_time_m_d_h_s(), "Good")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="function")
def add_destination_flag(context, api_test_client):
    api_test_client.flags.add_flag("Place " + utils.get_formatted_date_time_m_d_h_s(), "Destination")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="function")
def add_organisation_flag(context, api_test_client):
    api_test_client.flags.add_flag("Org " + utils.get_formatted_date_time_m_d_h_s(), "Organisation")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]
