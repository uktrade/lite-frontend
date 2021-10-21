import pytest

from copy import deepcopy
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:edit_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_edit_approve_advice_post(authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url):
    user_advice_create_url = f"/cases/{data_standard_case['case']['id']}/user-advice/"
    requests_mock.post(user_advice_create_url, json={})
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    data = {
        "approval_reasons": "meets the requirements updated",
        "instructions_to_exporter": "no specific instructions",
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history
    assert user_advice_create_url in history[3].url
    assert history[3].method == "POST"
    assert history[3].json() == [
        {
            "type": "approve",
            "text": "meets the requirements updated",
            "proviso": None,
            "note": "no specific instructions",
            "footnote_required": False,
            "footnote": None,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "denial_reasons": [],
        }
    ]


def test_edit_refuse_advice_post(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, refusal_advice, url
):
    user_advice_create_url = f"/cases/{data_standard_case['case']['id']}/user-advice/"
    requests_mock.post(user_advice_create_url, json={})
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = refusal_advice

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    requests_mock.get(
        client._build_absolute_uri("/static/denial-reasons/"),
        json={
            "denial_reasons": [
                {"id": "1"},
                {"id": "2"},
                {"id": "3"},
                {"id": "4"},
                {"id": "5"},
                {"id": "5a"},
                {"id": "5b"},
            ]
        },
    )

    data = {
        "refusal_reasons": "doesn't meet the requirement",
        "denial_reasons": ["3", "4", "5", "5a", "5b"],
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history
    assert user_advice_create_url in history[5].url
    assert history[5].method == "POST"
    assert history[5].json() == [
        {
            "type": "refuse",
            "text": "doesn't meet the requirement",
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
        }
    ]
