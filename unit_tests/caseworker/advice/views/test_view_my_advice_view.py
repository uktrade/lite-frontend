import pytest

from bs4 import BeautifulSoup
from copy import deepcopy
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:view_my_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_view_approve_advice_with_conditions_notes_and_nlr_products(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url
):
    """
    Tests display of the 'Approve all' advice given by the user with some conditions attached (proviso)
    and notes to the exporter. One of the product in this application is NLR so it also check
    if NLR products are listed on the page
    """
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table_rows = soup.find("table", id="table-licenceable-products-approve-all").find_all("tr")
    assert len(table_rows) == 3  # including header

    # Assert on Parties
    expected_headers = ["Country", "Type", "Name", "Approved products"]
    consignee = case_data["case"]["data"]["consignee"]
    expected_consignee_values = [consignee["country"]["name"], "Consignee", consignee["name"], "All"]
    end_user = case_data["case"]["data"]["end_user"]
    expected_end_user_values = [end_user["country"]["name"], "End user", end_user["name"], "All"]

    assert expected_headers == [column.text for column in table_rows[0].find_all("th")]
    assert expected_consignee_values == [column.text for column in table_rows[1].find_all("td")]
    assert expected_end_user_values == [column.text for column in table_rows[2].find_all("td")]

    # Assert Advice
    advice_content = [
        p.text for item in soup.findAll("div", {"class": "govuk-cookie-banner__content"}) for p in item.findAll("p")
    ]
    assert len(advice_content) == 3
    assert advice_content[0] == case_data["case"]["advice"][0]["text"]
    assert advice_content[1] == case_data["case"]["advice"][0]["proviso"]
    assert advice_content[2] == case_data["case"]["advice"][0]["note"]

    # Assert NLR - the second product on this application is NLR
    nlr_table_rows = soup.find("table", id="table-nlr-products").find_all("tr")
    assert ["Product name"] == [column.text for column in nlr_table_rows[0].find_all("th")]
    assert [case_data["case"]["data"]["goods"][1]["good"]["name"]] == [
        column.text for column in nlr_table_rows[1].find_all("td")
    ]


def test_view_refusal_advice_not_including_nlr_products(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, refusal_advice, url
):
    """
    Tests display of the 'Refuse all' advice given by the user and it doesn't include NLR products
    """
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = refusal_advice

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table_rows = soup.find("table", id="table-licenceable-products-refuse-all").find_all("tr")
    assert len(table_rows) == 3  # including header

    # Assert on Parties
    expected_headers = ["Country", "Type", "Name", "Refused products", "Refusal criteria"]
    consignee = case_data["case"]["data"]["consignee"]
    expected_consignee_values = [consignee["country"]["name"], "Consignee", consignee["name"], "All", "5a, 5b"]
    end_user = case_data["case"]["data"]["end_user"]
    expected_end_user_values = [end_user["country"]["name"], "End user", end_user["name"], "All", "5a, 5b"]

    assert expected_headers == [column.text for column in table_rows[0].find_all("th")]
    assert expected_consignee_values == [column.text for column in table_rows[1].find_all("td")]
    assert expected_end_user_values == [column.text for column in table_rows[2].find_all("td")]

    # Assert Advice
    advice_content = [
        p.text for item in soup.findAll("div", {"class": "govuk-cookie-banner__content"}) for p in item.findAll("p")
    ]
    assert len(advice_content) == 1
    assert advice_content[0] == case_data["case"]["advice"][0]["text"]

    # Assert NLR - the second product on this application is NLR
    nlr_table_rows = soup.find("table", id="table-nlr-products").find_all("tr")
    assert ["Product name"] == [column.text for column in nlr_table_rows[0].find_all("th")]
    assert [case_data["case"]["data"]["goods"][1]["good"]["name"]] == [
        column.text for column in nlr_table_rows[1].find_all("td")
    ]
