import os

from pytest import fixture


@fixture(scope="session")
def exporter_url(request):
    return "http://exporter:8300"


@fixture(scope="session")
def internal_url(request):
    return "http://caseworker:8200"


@fixture(scope="session")
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")


@fixture(scope="session")
def api_url(request):
    return os.environ.get(
        "LOCAL_LITE_API_URL",
        os.environ.get("LITE_API_URL"),
    )
