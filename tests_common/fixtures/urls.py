from pytest import fixture


@fixture()
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@fixture()
def internal_url(request):
    return request.config.getoption("--internal_url")


@fixture()
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")


@fixture()
def api_url(request):
    return request.config.getoption("--lite_api_url")
