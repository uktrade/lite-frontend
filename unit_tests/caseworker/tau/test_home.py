from bs4 import BeautifulSoup
import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_home_auth(authorized_client, url):
    """GET /tau should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_case_info(authorized_client, url):
    """GET /tau would return a case info panel"""
    response = authorized_client.get(url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="products-title").text == "Assessing 2 products"
    assert soup.find(id="case-details-title").text == "Case details"
    assert soup.find(id="products-section-title").text == "2 products"
    assert soup.find(id="destinations-section-title").text == "3 destinations"

    assert get_cells(soup, "table-products-1") == [
        "Select the type of firearm product",
        "",
        "Part number (optional)",
        "44",
        "Does the product have a government security grading or classification?",
        "No",
        "Is the product for military use?",
        "No",
        "Will the product be onward exported to any additional countries?",
        "No",
        "Quantity",
        "444",
        "Total value",
        "£888.00",
    ]
    assert get_cells(soup, "table-products-2") == [
        "Select the type of firearm product",
        "",
        "Part number (optional)",
        "44",
        "Does the product have a government security grading or classification?",
        "No",
        "Is the product for military use?",
        "No",
        "Will the product be onward exported to any additional countries?",
        "No",
        "Quantity",
        "444",
        "Total value",
        "£888.00",
    ]
    assert get_cells(soup, "table-products-summary") == ["", ""]
    assert get_cells(soup, "table-destinations") == [
        "United Kingdom",
        "end_user",
        "End User",
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "United Kingdom",
        "Third party",
        "Third party",
    ]
    assert get_cells(soup, "table-end-use") == ["44"]


def test_tau_home_noauth(client, url):
    """GET /tau should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302
