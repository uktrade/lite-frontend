import pytest

from pytest_django.asserts import assertTemplateUsed
from urllib import parse

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from caseworker.search.forms import ProductSearchForm


@pytest.fixture
def product_search_url():
    return reverse("search:products")


@pytest.fixture(autouse=True)
def mock_product_search(requests_mock, data_search):
    url = client._build_absolute_uri("/search/product/search/")
    return requests_mock.get(url=url, json=data_search)


def test_product_search_page(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assert response.status_code == 200


def test_product_search_renders_template(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assertTemplateUsed(response, "search/products.html")
    assertTemplateUsed(response, "layouts/base.html")


def test_product_search_view_get(authorized_client, product_search_url):
    response = authorized_client.get(product_search_url)
    assert response.status_code == 200

    assert isinstance(response.context["form"], ProductSearchForm)
    assertTemplateUsed(response, "search/products.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string == "Search products"
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Search"
    assert soup.find("input", {"name": "search_string"})


@pytest.mark.parametrize(
    "data",
    [
        ({"search_string": "Rifle", "page": 1}),
        ({"search_string": "Propellant, ML22", "page": 2}),
    ],
)
def test_product_search_run_query(authorized_client, product_search_url, requests_mock, data):
    response = authorized_client.get(
        product_search_url,
        data=data,
    )
    assert response.status_code == 200
    search_query = requests_mock.request_history[1]

    url = client._build_absolute_uri("/search/product/search/")
    query_params = f'{parse.urlencode({"search": data["search_string"], "page": data["page"]}, doseq=True)}'
    url = f"{url}?{query_params}"

    assert search_query.url == url
