from pytest import fixture
import shared.tools.helpers as utils
from shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_case_flag(driver, context, api_client_config):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.flags.add_flag("Case " + utils.get_formatted_date_time_m_d_h_s(), "Case")
    context.flag_name = lite_client.context["flag_name"]


@fixture(scope="function")
def add_good_flag(driver, context, api_client_config):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.flags.add_flag("Good " + utils.get_formatted_date_time_m_d_h_s(), "Good")
    context.flag_name = lite_client.context["flag_name"]


@fixture(scope="function")
def add_destination_flag(driver, context, api_client_config):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.flags.add_flag("Place " + utils.get_formatted_date_time_m_d_h_s(), "Destination")
    context.flag_name = lite_client.context["flag_name"]


@fixture(scope="function")
def add_organisation_flag(driver, context, api_client_config):
    lite_client = get_lite_client(context, api_client_config)
    lite_client.flags.add_flag("Org " + utils.get_formatted_date_time_m_d_h_s(), "Organisation")
    context.flag_name = lite_client.context["flag_name"]
