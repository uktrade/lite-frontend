import pytest

from copy import deepcopy
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(f"cases:edit_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


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
    history = [item for item in requests_mock.request_history if user_advice_create_url in item.url]
    assert len(history) == 1
    history = history[0]
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "note": "no specific instructions",
            "proviso": "",
            "text": "meets the requirements updated",
            "type": "approve",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


def test_edit_refuse_advice_post(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    refusal_advice,
    url,
    mock_denial_reasons,
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

    data = {
        "refusal_reasons": "doesn't meet the requirement",
        "denial_reasons": ["3", "4", "5", "5a", "5b"],
    }
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert user_advice_create_url in history.url
    assert history.method == "POST"
    assert history.json() == [
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "type": "refuse",
        },
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "footnote_required": False,
            "text": "doesn't meet the requirement",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
        },
        {
            "denial_reasons": ["3", "4", "5", "5a", "5b"],
            "footnote_required": False,
            "good": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
            "text": "doesn't meet the requirement",
            "type": "refuse",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "d4feac1e-851d-41a5-b833-eb28addb8547",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]
