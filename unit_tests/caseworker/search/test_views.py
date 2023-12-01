import pytest
import json

from pytest_django.asserts import assertTemplateUsed
from urllib import parse

from bs4 import BeautifulSoup
from django.urls import reverse

import re

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
    product_search_result_table = soup.find_all("table")[0]

    headers = [header.text.strip() for header in product_search_result_table.find_all("th")]
    assert headers == [
        "Case reference",
        "Assessment date",
        "Destination",
        "Control entry",
        "Regime",
        "Report summary",
        "Assessment notes",
        "TAU assessor",
        "Quantity",
        "Value",
    ]

    distinct_combination_hits_tbody = product_search_result_table.find_all("tbody")[0]
    data = [col.text.strip() for col in distinct_combination_hits_tbody.find_all("td")]
    assert data == [
        "GBSIEL/2020/0000001/P",
        "12 September 2023",
        "France",
        "ML1a",
        "",
        "guns",
        "no concerns",
        "Firstname Lastname",  # /PS-IGNORE
        "1 item",
        "£1,000.00",
    ]

    show_more_cases_tbody = product_search_result_table.find_all("tbody")[1]
    data = [col.text.strip() for col in show_more_cases_tbody.find_all("td")]
    assert data == [
        "GBSIEL/2020/0000001/P",
        "12 October 2023",
        "Germany",
        "ML1a",
        "",
        "guns",
        "no concerns",
        "Firstname Lastname",  # /PS-IGNORE
        "1 item",
        "£1,000.00",
    ]

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
    # based on distinct combination (control entry, report summary, regime) so extract the first one
    result = response.context["search_results"]["results"][0]["distinct_combination_hits"][0]
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
        [
            "assessment_date",
            "destination",
            "control_entry",
            "regime",
            "report_summary",
            "assessment_notes",
            "tau_assessor",
            "quantity",
            "value",
        ],
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
                {"label": "TAU assessor", "key": "tau_assessor", "default_visible": False},
                {"label": "Quantity", "key": "quantity", "default_visible": False},
                {"label": "Value", "key": "value", "default_visible": False},
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


@pytest.mark.parametrize(
    ("input_data", "results", "remaining_hits_visible_count"),
    [
        (
            {"search_string": "hybrid", "page": 1},
            {
                "count": 1,
                "results": [
                    {
                        "inner_hits": {
                            "hits": [
                                {
                                    "id": "e6ed3baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "hybrid shotriflegun",
                                    "control_list_entries": [{"rating": "ML1a"}],
                                    "report_summary": "sporting shotguns",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                                {
                                    "id": "12343baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "hybrid shotriflegun",
                                    "control_list_entries": [{"rating": "ML1a"}],
                                    "report_summary": "sporting shotguns",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                            ]
                        },
                    }
                ],
            },
            1,
        ),
        (
            {"search_string": "hybrid", "page": 1},
            {
                "count": 1,
                "results": [
                    {
                        "inner_hits": {
                            "hits": [
                                {
                                    "id": "e6ed3baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "hybrid shotriflegun",
                                    "control_list_entries": [{"rating": "ML1a"}],
                                    "report_summary": "sporting shotguns",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                                {
                                    "id": "12343baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "hybrid shotriflegun",
                                    "control_list_entries": [{"rating": "ML1a"}],
                                    "report_summary": "sporting guns",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                            ]
                        },
                    }
                ],
            },
            0,
        ),
        (
            {"search_string": "liquid", "page": 1},
            {
                "count": 1,
                "results": [
                    {
                        "inner_hits": {
                            "hits": [
                                {
                                    "id": "e6ed3baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "orange red liquid",
                                    "control_list_entries": [{"rating": "1C35064"}],
                                    "report_summary": "chemicals used for industrial/commercial processes",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                                {
                                    "id": "12343baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "orange red liquid",
                                    "control_list_entries": [{"rating": "1C35064"}],
                                    "report_summary": "chemicals used for industrial/commercial processes",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                            ]
                        },
                    }
                ],
            },
            1,
        ),
        (
            {"search_string": "liquid", "page": 1},
            {
                "count": 1,
                "results": [
                    {
                        "inner_hits": {
                            "hits": [
                                {
                                    "id": "e6ed3baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "orange red liquid",
                                    "control_list_entries": [{"rating": "1C35064"}],
                                    "report_summary": "chemicals used for industrial/commercial processes",
                                    "regime_entries": [],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                                {
                                    "id": "12343baa-4d37-4d2b-be40-bbbe99555fb6",  # /PS-IGNORE
                                    "name": "orange red liquid",
                                    "control_list_entries": [{"rating": "1C35064"}],
                                    "report_summary": "chemicals used for industrial/commercial processes",
                                    "regime_entries": [{"name": "AG Chemical List"}],
                                    "application": {
                                        "id": "f5bc54bf-323d-4de1-ae98-ef9f1894c5f3",  # /PS-IGNORE
                                        "reference_code": "GBSIEL/2020/0000001/P",
                                    },
                                    "quantity": 1.0,
                                    "value": 1.0,
                                },
                            ]
                        },
                    }
                ],
            },
            0,
        ),
    ],
)
def test_group_results_by_combination(
    authorized_client, requests_mock, product_search_url, input_data, results, remaining_hits_visible_count
):
    """
    Test whether the results are grouped i.e. whether the summary (dropdown) component appears for certain kinds of search results.
    (1) Two similar products with matching control entry, report summary
    (2) Two similar products with matching control entry, but different report summary
    (3) Two similar products with matching control entry, report summary, regime
    (4) Two similar products with matching control entry and report summary but different regime
    """
    url = client._build_absolute_uri("/search/product/search/")
    requests_mock.get(
        url=url,
        json=results,
    )

    response = authorized_client.get(product_search_url, input_data)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    remaining_hits_tbody_list = soup.find_all("tbody", class_="table-expander__remaining-hits")
    assert len(remaining_hits_tbody_list) == remaining_hits_visible_count
