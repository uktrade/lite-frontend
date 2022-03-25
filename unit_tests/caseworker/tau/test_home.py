from bs4 import BeautifulSoup
from django.urls import reverse
import pytest

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_get_control_list_entries(requests_mock):
    url = client._build_absolute_uri("/static/control-list-entries/")
    yield requests_mock.get(
        url=url,
        json={
            "control_list_entries": [
                {"rating": "A", "text": "A"},
                {"rating": "B", "text": "B"},
                {"rating": "C", "text": "C"},
                {"rating": "D", "text": "D"},
            ]
        },
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_home_auth(authorized_client, url, mock_get_control_list_entries):
    """GET /tau should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_case_info(authorized_client, url, mock_get_control_list_entries):
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


def test_form(authorized_client, url, data_standard_case, requests_mock, mock_get_control_list_entries):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=data_standard_case)
    requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )
    # unassessed products should have 1 entry
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert good["id"] in soup.find(id="unassessed-products").text
    response = authorized_client.post(
        url, data={"report_summary": "test", "goods": [good["id"]], "does_not_have_control_list_entries": True}
    )
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary": "test",
        "comment": "",
        "current_object": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["8b730c06-ab4e-401c-aeb0-32b3c92e912c"],
        "is_good_controlled": False,
    }
