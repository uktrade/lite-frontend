from pytest import fixture


@fixture(scope="session")
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@fixture(scope="session")
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")


@fixture(scope="session")
def api_url(request):
    return request.config.getoption("--lite_api_url")
