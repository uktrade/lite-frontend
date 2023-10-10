import pytest
from django.http import Http404
from core.helpers import convert_parameters_to_query_params, check_url


@pytest.fixture
def mock_request(rf):
    request = rf.get("/", SERVER_NAME="testserver")
    return request


def test_convert_parameters_to_query_params():
    params = {"request": "request", "org_type": ["individual", "commercial"], "page": 1, "empty": None}

    assert convert_parameters_to_query_params(params) == "?org_type=individual&org_type=commercial&page=1"


@pytest.mark.parametrize("url", ["/next-url/", "http://testserver/next-url/"])
def test_check_url(mock_request, url):
    assert check_url(mock_request, url) == url


# Check not valid host and non secure url
@pytest.mark.parametrize("url", ["http://not-the-same.com/next/", "https://test-server/next/"])
def test_check_url_not_allowed(mock_request, url):
    with pytest.raises(Http404):
        check_url(mock_request, url)
