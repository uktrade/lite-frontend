import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import FCDO_CASES_TO_REVIEW_QUEUE, FCDO_TEAM
from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:view_my_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def advice(current_user):
    return [
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
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


@pytest.fixture(params=(None, "cd2263b4-a427-4f14-8552-505e1d192bb8"))
def advice_with_and_without_consignee(request, advice):
    """This is a parametrized fixture that returns advice for 1/2 destinations
    followed by advice for both destinations. Nothing clever here, for the former,
    we just miss the consignee while keeping everything else the same.
    """
    for item in advice:
        item["consignee"] = request.param
    return advice


@pytest.fixture
def refusal_advice(request, advice):
    for item in advice:
        item["type"] = {"key": "refuse", "value": "Refuse"}
        item["denial_reasons"] = ["5a", "5b"]
    return advice


def test_view_approve_advice_with_conditions_notes_and_nlr_products(
    authorized_client, requests_mock, data_standard_case, advice, url
):
    """
    Tests display of the 'Approve all' advice given by the user with some conditions attached (proviso)
    and notes to the exporter. One of the product in this application is NLR so it also check
    if NLR products are listed on the page
    """
    data_standard_case["case"]["advice"] = advice
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == ["Country", "Type", "Name", "Approved products"]
    # checking for 2 times because the same user gave advice twice
    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "United Kingdom",
        "End-user",
        "End User",
        "All",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
    ] * 2


def test_view_refusal_advice_not_including_nlr_products(
    authorized_client, requests_mock, data_standard_case, refusal_advice, url
):
    """
    Tests display of the 'Refuse all' advice given by the user and it doesn't include NLR products
    """
    data_standard_case["case"]["advice"] = refusal_advice
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == [
        "Country",
        "Type",
        "Name",
        "Refused products",
        "Refusal criteria",
    ]
    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "five a, five b",
        "United Kingdom",
        "End-user",
        "End User",
        "All",
        "five a, five b",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
        "five a, five b",
    ] * 2


def test_move_case_forward(
    mock_gov_user, authorized_client, requests_mock, data_standard_case, queue_pk, advice_with_and_without_consignee
):
    url = reverse(
        "cases:view_my_advice",
        kwargs={"queue_pk": "f458094c-1fed-4222-ac70-ff5fa20ff649", "pk": data_standard_case["case"]["id"]},
    )
    mock_gov_user["user"]["team"]["alias"] = FCDO_TEAM
    advice_with_and_without_consignee[0]["user"]["team"]["alias"] = FCDO_TEAM
    data_standard_case["case"]["advice"] = advice_with_and_without_consignee
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    requests_mock.put(client._build_absolute_uri(f"/cases/{case_id}/assigned-queues/"), json={"queues": [queue_pk]})

    response = authorized_client.get(url)
    assert response.status_code == 200
    advice_completed = advice_with_and_without_consignee.pop()["consignee"] is not None
    assert response.context["advice_completed"] == advice_completed
    # Check if the MoveCaseForwardForm is rendered only when advice_completed
    soup = BeautifulSoup(response.content, "html.parser")
    assert len(soup.find_all("form")) == (1 if advice_completed else 0)
    # We do not show the "Move Case Forward" button in the template when advice_completed
    # is False but we haven't put any checks on the server that stops this, which is why
    # the following works whether advice_completed is True or not -
    response = authorized_client.post(url)
    assert response.status_code == 302
