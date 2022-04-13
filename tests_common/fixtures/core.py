from pytest import fixture

from ..api_client.api_client import ApiClient
from ..api_client.libraries.request_data import build_request_data
from ..api_client.sub_helpers.users import create_great_sso_user
from ..tools.utils import build_test_helper

MAX_WORKERS = 3


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def exporter_info(request, environment):
    return create_great_sso_user()


@fixture(scope="session")
def internal_info(request, environment, worker_id):
    # For parallel execution, ensure that a TEST_SSO_EMAIL_n and TEST_SSO_PASSWORD_n
    # pair of environment variables exist for each worker. n is zero-based and is
    # controlled with the -n command line option.
    try:
        worker_num = int(worker_id[2:])
    except ValueError:
        worker_num = 0

    if (worker_num + 1) > MAX_WORKERS:
        raise RuntimeError(f"Can only support {MAX_WORKERS} parallel workers")

    email = environment(f"TEST_SSO_EMAIL_{worker_num}", default=environment("TEST_SSO_EMAIL"))
    password = environment(f"TEST_SSO_PASSWORD_{worker_num}", default=environment("TEST_SSO_PASSWORD"))

    first_name, last_name = environment("TEST_SSO_NAME").split(" ")
    return {
        "email": email,
        "name": environment("TEST_SSO_NAME"),
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }


@fixture(scope="session")
def api_client(request, exporter_info, internal_info, context, environment):
    api_url = request.config.getoption("--lite_api_url")
    base_url = api_url.rstrip("/")
    request_data = build_request_data(exporter_user=exporter_info, gov_user=internal_info)
    api_client = ApiClient(base_url, request_data, {})

    if environment("BASIC_AUTH_ENABLED", default="False") == "True":
        hosts = environment("BROWSER_HOSTS").replace("${ENVIRONMENT}", environment("ENVIRONMENT")).split(",")
        for host in hosts:
            api_client.auth_basic(environment("AUTH_USER_NAME"), environment("AUTH_USER_PASSWORD"))
            response = api_client.session.request("GET", f"https://{host}{environment('ENDPOINT')}")
            response.raise_for_status()
    return api_client


@fixture(scope="session")
def api_test_client(api_client, context):
    return build_test_helper(api_client)
