import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def default_feature_flag(settings):
    settings.FEATURE_FLAG_PRODUCT_SEARCH = True


@pytest.fixture
def product_search_url():
    return reverse("search:products")


@pytest.fixture(autouse=True)
def mock_product_search(requests_mock, data_search):
    url = client._build_absolute_uri("/search/product/search/")
    return requests_mock.get(url=url, json=data_search)


def test_product_search_disabled_feature_flag(
    authorized_client,
    product_search_url,
    settings,
):
    settings.FEATURE_FLAG_PRODUCT_SEARCH = False
    response = authorized_client.get(product_search_url)
    assert response.status_code == 404


def test_product_search_enabled_feature_flag(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assert response.status_code == 200


def test_product_search_renders_template(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assertTemplateUsed(response, "search/products.html")
    assertTemplateUsed(response, "layouts/base.html")


def test_product_search_search_results_no_querystring(
    authorized_client,
    product_search_url,
    mock_product_search,
    data_search,
):
    response = authorized_client.get(product_search_url)
    assert mock_product_search.called_once
    assert mock_product_search.last_request.qs == {}

    search_results = response.context["search_results"]
    assert search_results == data_search


def test_product_search_search_results_querystring(
    authorized_client,
    product_search_url,
    mock_product_search,
    data_search,
):
    response = authorized_client.get(f"{product_search_url}?q=test")
    assert mock_product_search.called_once
    assert mock_product_search.last_request.qs == {
        "q": ["test"],
    }

    search_results = response.context["search_results"]
    assert search_results == data_search
