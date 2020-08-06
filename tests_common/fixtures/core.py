import logging
import os
from http import HTTPStatus
from pytest import fixture

from ..api_client.api_client import ApiClient
from ..api_client.libraries.request_data import build_request_data
from ..api_client.sub_helpers.users import post_user_to_great_sso
from ..tools.utils import get_or_create_attr, build_test_helper

AUTH_USER_NAME = os.environ.get("AUTH_USER_NAME")
AUTH_USER_PASSWORD = os.environ.get("AUTH_USER_PASSWORD")
ENDPOINT = os.environ.get("ENDPOINT")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
TEST_HOSTS = os.environ.get("BROWSER_HOSTS")


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
def api_client(request, exporter_info, internal_info):
    api_url = request.config.getoption("--lite_api_url")
    base_url = api_url.rstrip("/")
    request_data = build_request_data(exporter_user=exporter_info, gov_user=internal_info)
    api_client = ApiClient(base_url, request_data, {})
    if os.getenv("TEST_TYPE_BROWSER_STACK", "False") == "True":
        test_hosts = list(TEST_HOSTS.replace("${ENVIRONMENT}", ENVIRONMENT).split(","))
        for host in test_hosts:
            logging.debug("Allowing test runner access to %s", host)
            api_client.auth_basic(AUTH_USER_NAME, AUTH_USER_PASSWORD)
            response = api_client.session.request("GET", f"https://{host}{ENDPOINT}")
            assert response.status_code == HTTPStatus.OK
            assert response.text == "ok"

    return get_or_create_attr(context, "api_client", api_client)


@fixture(scope="session")
def api_test_client(api_client):
    return get_or_create_attr(context, "api_test_client", build_test_helper(api_client))
