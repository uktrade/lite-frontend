import pytest
import requests

from caseworker.search import services


@pytest.fixture
def default_request(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request


def test_get_product_search_results_default_no_order(mock_product_search, default_request):
    services.get_product_search_results(request=default_request, query_params={})

    assert mock_product_search.request_history[0].qs == {}


def test_get_product_search_results_default_no_order(mock_product_search, default_request):
    services.get_product_search_results(request=default_request, query_params={"term": "foo"})

    assert mock_product_search.request_history[0].qs == {"term": ["foo"], "ordering": ["canonical_name"]}
