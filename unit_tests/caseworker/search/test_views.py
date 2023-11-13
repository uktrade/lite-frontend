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


def test_product_search_view_get(authorized_client, product_search_url, mock_product_search):
    response = authorized_client.get(product_search_url)
    assert response.status_code == 200

    assert isinstance(response.context["form"], ProductSearchForm)
    assertTemplateUsed(response, "search/products.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string == "Search products"
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Search"
    assert soup.find("input", {"name": "search_string"})

    expected_fields = {
        "id",
        "name",
        "description",
        "part_number",
        "destination",
        "application",
        "date",
        "queues",
        "organisation",
        "control_list_entries",
        "ratings",
        "report_summary",
        "assessment_note",
        "assessment_date",
        "assessed_by",
        "regime_entries",
        "regimes",
    }
    # check for presence of expected fields in search results
    # We have a fixture with example search results and currently we group them
    # based on unique rating so extract the first one
    result = response.context["search_results"]["results"][0]["distinct_rating_hits"][0]
    actual_fields = set(result.keys())

    assert expected_fields == actual_fields


@pytest.mark.parametrize(
    "data, expected_query_params",
    [
        ({"page": 1}, {"search": "", "page": 1}),
        ({"search_string": "Rifle", "page": 1}, {"search": "Rifle", "page": 1}),
        ({"search_string": "Propellant, ML22", "page": 2}, {"search": "Propellant, ML22", "page": 2}),
    ],
)
def test_product_search_run_query(authorized_client, product_search_url, requests_mock, data, expected_query_params):
    response = authorized_client.get(
        product_search_url,
        data=data,
    )
    assert response.status_code == 200
    search_query = requests_mock.request_history[1]

    url = client._build_absolute_uri("/search/product/search/")
    url = f"{url}?{parse.urlencode(expected_query_params, doseq=True)}"

    assert search_query.url == url
