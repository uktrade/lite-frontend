from pytest import fixture
import shared.tools.helpers as utils


def get_flag_of_level(flags, level):
    return next(
        iter(
            [
                item
                for item in flags
                if item["level"] == level
                and item["status"] == "Active"
                and item["team"]["name"] == "Admin"
                and item["blocks_approval"] is not True
            ]
        ),
        None,
    )


def get_or_create_flag_of_level(level, api_test_client, context):
    all_flags = api_test_client.flags.get_list_of_flags()
    flag = get_flag_of_level(all_flags, level)
    if not flag:
        flag = api_test_client.flags.add_flag(level + " " + utils.get_formatted_date_time_y_m_d_h_s(), level)
    context.flag_name = flag["name"]
    context.flag_id = flag["id"]


@fixture(scope="module")
def add_case_flag(context, api_test_client):
    get_or_create_flag_of_level("Case", api_test_client, context)


@fixture(scope="module")
def add_good_flag(context, api_test_client):
    get_or_create_flag_of_level("Good", api_test_client, context)


@fixture(scope="module")
def add_destination_flag(context, api_test_client):
    get_or_create_flag_of_level("Destination", api_test_client, context)


@fixture(scope="module")
def add_organisation_flag(context, api_test_client):
    get_or_create_flag_of_level("Organisation", api_test_client, context)
