from bs4 import BeautifulSoup
from django.urls import reverse
import pytest

from core import client
from caseworker.tau import views


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture()
def gov_user():
    return {
        "user": {
            "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "team": {
                "id": "211111b-c111-11e1-1111-1111111111a",
                "name": "Test",
                "alias": "TEST_1",
            },
        }
    }


def get_cells(soup, table_id):
    return [td.text.strip() for td in soup.find(id=table_id).find_all("td")]


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
    good["firearm_details"]["year_of_manufacture"] = "1930"

    response = authorized_client.get(url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="subtitle").text == "Assess 1 product going from Great Britain to Abu Dhabi and United Kingdom"
    assert get_cells(soup, "assessed-products") == [
        "2.",
        "p2",
        "",
        "No",
        "",
        "scale compelling technologies",
        "test assesment note",
        "Edit",
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
    assert edit_url == soup.find(id="assessed-products").find("tbody").find("a").attrs["href"]

    # Test if the unassessed products table is sane
    assert get_cells(soup, "table-products-1") == [
        "Product document (PDF, opens in new tab)",
        "",
        "Select the type of firearm product",
        "Firearms",
        "Part number (optional)",
        "44",
        "Does the product have a government security grading or classification?",
        "Yes",
        "Enter a prefix (optional)",
        "NATO",
        "What is the security grading or classification?",
        "Official",
        "Enter a suffix (optional)",
        "SUFFIX",
        "Name and address of the issuing authority",
        "Government entity",
        "Reference",
        "GR123",
        "Date of issue",
        "20 February 2020",
        "What is the calibre of the product?",
        "0.25",
        "Is the product a replica firearm?",
        "No",
        "What year was it made?",
        "1930",
        "Will the product be incorporated into another item before it is onward exported?",
        "N/A",
        "Has the product been deactivated?",
        "No",
        "Number of items",
        "2",
        "Total value",
        "£444.00",
        "Will each product have a serial number or other identification marking?",
        "Yes, I can add serial numbers now",
        "Enter serial numbers or other identification markings",
        "View serial numbers\n            \n\n\n            \n                1. 12345   \n            \n                2. ABC-123",
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

    data = {
        "report_summary": "test",
        "goods": [good["id"]],
        "does_not_have_control_list_entries": True,
    }

    response = authorized_client.post(url, data=data)
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


@pytest.mark.parametrize(
    "team_alias, team_name",
    (
        (views.TAU_ALIAS, "TAU"),
        ("Not TAU", "Some other team"),
    ),
)
def test_move_case_forward(
    requests_mock,
    authorized_client,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    gov_user,
    team_alias,
    team_name,
):
    """
    When all products has been assessed, we will get a move-case-forward form.
    """
    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(url)
    assert response.context["unassessed_goods"] == []

    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form")
    if team_alias == views.TAU_ALIAS:
        assert len(forms) == 1
        assert forms[0].attrs["action"] == reverse(
            "cases:tau:move_case_forward",
            kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
        )
    else:
        assert len(forms) == 0
