from pytest import fixture


@fixture(scope="module")
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@fixture(scope="module")
def internal_url(request):
    return request.config.getoption("--internal_url")


@fixture(scope="module")
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")
