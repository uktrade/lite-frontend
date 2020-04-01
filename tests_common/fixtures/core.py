from pytest import fixture

from ..api_client.api_client import ApiClient
from ..api_client.libraries.request_data import build_request_data
from ..api_client.sub_helpers.users import post_user_to_great_sso
from ..api_client.test_helper import build_test_helper
from ..tools.utils import get_or_create_attr


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def exporter_info(request, environment):
    response = post_user_to_great_sso()
    return {
        "email": response["email"],
        "password": response["password"],
        "first_name": response["first_name"],
        "last_name": response["last_name"],
    }


@fixture(scope="session")
def internal_info(request, environment):
    gov_user_email = environment("TEST_SSO_EMAIL")
    name = environment("TEST_SSO_NAME")
    gov_user_first_name, gov_user_last_name = name.split(" ")
    gov_user_password = environment("TEST_SSO_PASSWORD")

    return {
        "email": gov_user_email,
        "name": name,
        "first_name": gov_user_first_name,
        "last_name": gov_user_last_name,
        "password": gov_user_password,
    }


@fixture(scope="session")
def api_test_client(request, exporter_info, internal_info):
    api_url = request.config.getoption("--lite_api_url")
    base_url = api_url.rstrip("/")
    request_data = build_request_data(exporter_user=exporter_info, gov_user=internal_info)
    api_client = ApiClient(base_url, request_data, {})

    return get_or_create_attr(context, "api", build_test_helper(api_client))
