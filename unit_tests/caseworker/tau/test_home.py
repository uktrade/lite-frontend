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


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_home_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET /tau should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.skip("The /tau view doesn't return case details anymore but it might in the future")
def test_case_info(authorized_client, url, mock_control_list_entries, mock_precedents_api):
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


def test_home_content(
    authorized_client, url, data_queue, data_standard_case, mock_control_list_entries, mock_precedents_api
):
    """GET /tau would return a case info panel"""
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []

    response = authorized_client.get(url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="subtitle").text == "Assess 1 product(s) going from Great Britain to Abu Dhabi, United Kingdom"
    assert get_cells(soup, "assessed-products") == [
        "2",
        "p2",
        "444",
        "",
        "No",
        "scale compelling technologies",
        "Edit assessment",
    ]

    # Test if the link to edit assessed-products is sane
    assessed_good_id = data_standard_case["case"]["data"]["goods"][1]["id"]
    edit_url = reverse(
        "cases:tau:edit",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
            "good_id": assessed_good_id,
        },
    )
    assert edit_url == soup.find(id="assessed-products").find("a").attrs["href"]

    # Test if the unassessed products table is sane
    assert get_cells(soup, "table-products-1") == [
        "Select the type of firearm product",
        "Firearms",
        "Part number (optional)",
        "44",
        "Does the product have a government security grading or classification?",
        "Yes",
        "Is the product for military use?",
        "No",
        "Will the product be onward exported to any additional countries?",
        "No",
        "Quantity",
        "444",
        "Total value",
        "£0.00",
    ]

    # The precedent for the unassessed product
    assert get_cells(soup, "table-precedents-1") == [
        "Reference",
        "GBSIEL/2020/0002687/T",
        "Control list entry",
        "ML1a",
        "Regime",
        "",
        "Report summary",
        "test-report-summary",
        "Quantity",
        "10",
        "Destinations",
        "GB",
    ]


def test_tau_home_noauth(client, url):
    """GET /tau should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client, url, data_standard_case, requests_mock, mock_control_list_entries, mock_precedents_api
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )
    # unassessed products should have 1 entry
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    unassessed_products = soup.find(id="unassessed-products").find_all("input")
    assert len(unassessed_products) == 1
    assert unassessed_products[0].attrs["value"] == good["id"]
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
        "is_wassenaar": False,
    }


def test_move_case_forward(
    authorized_client, url, data_queue, data_standard_case, mock_control_list_entries, mock_precedents_api
):
    """
    When all products has been assessed, we will get a move-case-forward form.
    """
    response = authorized_client.get(url)
    assert response.context["unassessed_goods"] == []

    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form")
    assert len(forms) == 1
    assert forms[0].attrs["action"] == reverse(
        "cases:tau:move_case_forward",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )
