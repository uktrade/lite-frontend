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


@pytest.fixture(params=(None, "cd2263b4-a427-4f14-8552-505e1d192bb8"))
def advice(request, current_user):
    """This is a parametrized fixture that returns advice for 1/2 destinations
    followed by advice for both destinations. Nothing clever here, for the former,
    we just miss the consignee while keeping everything else the same.
    """
    return [
        {
            "consignee": request.param,
            "country": None,
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "footnotes",
            "good": good_id,
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",
            "level": "user",
            "note": "additional notes",
            "proviso": "no conditions",
            "text": "meets the criteria",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": current_user,
        }
        for good_id in ("0bedd1c3-cf97-4aad-b711-d5c9a9f4586e", "6daad1c3-cf97-4aad-b711-d5c9a9f4586e")
    ]


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


def test_move_case_forward(authorized_client, requests_mock, data_standard_case, queue_pk, advice, url):
    data_standard_case["case"]["advice"] = advice
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_id}/assigned-queues/"), json={"queues": [queue_pk]})
    response = authorized_client.get(url)
    assert response.status_code == 200
    advice_completed = advice.pop()["consignee"] is not None
    assert response.context["advice_completed"] == advice_completed
    # Check if the MoveCaseForwardForm is rendered only when advice_completed
    soup = BeautifulSoup(response.content, "html.parser")
    assert len(soup.find_all("form")) == (1 if advice_completed else 0)
    # We do not show the "Move Case Forward" button in the template when advice_completed
    # is False but we haven't put any checks on the server that stops this, which is why
    # the following works whether advice_completed is True or not -
    response = authorized_client.post(url)
    assert response.status_code == 302
