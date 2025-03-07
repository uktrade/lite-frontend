import pytest

from ..api_client.api_client import ApiClient
from ..api_client.libraries.request_data import build_request_data
from ..api_client.sub_helpers.users import create_govuk_sso_user
from ..tools.utils import build_test_helper


@pytest.fixture()
def context(request):
    class Context(object):
        pass

    return Context()


@pytest.fixture()
def exporter_info(request, environment):
    return create_govuk_sso_user()


@pytest.fixture()
def internal_info(request, environment):
    return {
        "email": "lite-ops@digital.trade.gov.uk",  # /PS-IGNORE
        "name": "Test User",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture()
def api_client(request, exporter_info, internal_info, api_url, context, environment):
    base_url = api_url.rstrip("/")
    request_data = build_request_data(exporter_user=exporter_info, gov_user=internal_info)
    api_client = ApiClient(base_url, request_data, {})
    return api_client


@pytest.fixture()
def api_test_client(api_client, context):
    return build_test_helper(api_client)
