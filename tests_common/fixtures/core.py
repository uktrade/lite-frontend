from pytest import fixture

from ..api_client.api_client import ApiClient
from ..api_client.libraries.request_data import build_request_data


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def exporter_info(request, environment):
    exporter_sso_email = environment("TEST_EXPORTER_SSO_EMAIL")
    name = environment("TEST_EXPORTER_SSO_NAME")
    first_name, last_name = name.split(" ")
    exporter_sso_password = environment("TEST_EXPORTER_SSO_PASSWORD")

    return {
        "email": exporter_sso_email,
        "password": exporter_sso_password,
        "first_name": first_name,
        "last_name": last_name,
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


# TODO: this will be renamed to api_client however this requires changes
# to exporter and internal FE's and will be done as the next step
@fixture(scope="session")
def api_client_config(request, exporter_info, internal_info):
    api_url = request.config.getoption("--lite_api_url")
    base_url = api_url.rstrip("/")
    request_data = build_request_data(exporter_user=exporter_info, gov_user=internal_info)
    api_client = ApiClient(base_url, request_data, {})

    return {"api_url": api_url, "exporter": exporter_info, "gov": internal_info, "the_client": api_client}
