import pytest
import json

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

    # Each search result is displayed as a table
    # check that expected fields are displayed with expected values
    table = soup.find("table")
    table_rows = table.findAll("tr")
    headers = [header.text.strip() for header in table_rows[0].find_all("th")]
    assert headers == [
        "Case reference",
        "Assessment date",
        "Destination",
        "Control entry",
        "Regime",
        "Report summary",
        "Assessment notes",
    ]
    data = [col.text.strip() for col in table_rows[1].find_all("td")]
    assert data == ["GBSIEL/2020/0000001/P", "12 September 2023", "France", "ML1a", "", "guns", "no concerns"]

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

    assert expected_fields.issubset(actual_fields)


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


@pytest.mark.parametrize(
    ("expected_data_customiser_keys"),
    [
        ["assessment_date", "destination", "control_entry", "regime", "report_summary", "assessment_notes"],
    ],
)
def test_product_search_columns_are_toggleable(product_search_url, authorized_client, expected_data_customiser_keys):
    response = authorized_client.get(product_search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # check th elements
    actual_data_customiser_keys = [
        th.attrs["data-customiser-key"]
        for th in soup.find(id="product-search-customiser").find_all("th", class_="govuk-table__header")
        if "data-customiser-key" in th.attrs.keys()
    ]
    assert set(expected_data_customiser_keys) == set(actual_data_customiser_keys)
    # check td elements
    actual_data_customiser_keys = [
        td.attrs["data-customiser-key"]
        for td in soup.find(id="product-search-customiser").find_all("td", class_="govuk-table__cell")
        if "data-customiser-key" in td.attrs.keys()
    ]
    assert set(expected_data_customiser_keys) == set(actual_data_customiser_keys)


@pytest.mark.parametrize(
    ("expected_data_customiser_spec"),
    [
        {
            "options_label": "Customise search results",
            "identifier": "product-search-view",
            "analytics_prefix": "psv",
            "options_hint": "Select columns to show",
            "toggleable_elements": [
                {"label": "Assessment date", "key": "assessment_date", "default_visible": True},
                {"label": "Destination", "key": "destination", "default_visible": True},
                {"label": "Control entry", "key": "control_entry", "default_visible": True},
                {"label": "Regime", "key": "regime", "default_visible": True},
                {"label": "Report summary", "key": "report_summary", "default_visible": True},
                {"label": "Assessment notes", "key": "assessment_notes", "default_visible": True},
            ],
        }
    ],
)
def test_product_search_data_customiser_spec(authorized_client, product_search_url, expected_data_customiser_spec):
    """
    We can't directly test if the columns are visible or not using BeautifulSoup, as it just parses the html and is not a browser. Therefore we just check if
    the data-customiser-spec is as expected. The data-customiser-spec is where column visibility is set. The customiser.js component has its own tests so we
    don't need to duplicate those tests here. Instead we test that, assuming customiser js is working, we have the spec set correctly.
    """
    response = authorized_client.get(product_search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    expected_data_customiser_spec_string = str(json.dumps(expected_data_customiser_spec))
    actual_data_customiser_spec_string = str(soup.find(id="product-search-customiser").attrs["data-customiser-spec"])
    assert expected_data_customiser_spec_string == actual_data_customiser_spec_string
