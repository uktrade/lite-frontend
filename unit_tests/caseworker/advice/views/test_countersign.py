import pytest

from copy import deepcopy
from django.urls import reverse

from core import client
from caseworker.advice import services


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_countersign_approve_all_put(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    mock_gov_user,
    url,
):
    case_id = data_standard_case["case"]["id"]
    user_id = mock_gov_user["user"]["id"]

    # Set up advice on the case
    data_standard_case["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    data_standard_case["case"]["advice"] = advice_for_countersign

    # Setup mock API requests
    countersign_advice_url = client._build_absolute_uri(f"/cases/{case_id}/countersign-advice/")
    requests_mock.put(countersign_advice_url, json={})
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    requests_mock.get(client._build_absolute_uri(f"/gov_users/{user_id}"), json=mock_gov_user)
    requests_mock.get(client._build_absolute_uri(f"/users/{mock_gov_user['user']['id']}/"), json={})

    advice_to_countersign = services.get_advice_to_countersign(advice_for_countersign, mock_gov_user["user"])

    case_queues_url = client._build_absolute_uri(f"/cases/{case_id}/queues/")
    requests_mock.put(case_queues_url, json={})

    data = {
        "form-TOTAL_FORMS": [f"{len(advice_to_countersign)}"],
        "form-INITIAL_FORMS": ["0"],
        "form-MIN_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "form-MAX_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "submit": ["Submit"],
    }

    for index, item in enumerate(advice_to_countersign.keys()):
        data[f"form-{index}-approval_reasons"] = [f"reason{index}"]
        requests_mock.get(client._build_absolute_uri(f"/users/{item}/team-queues/"), json={"queues": []})

    response = authorized_client.post(url, data=data)
    assert response.status_code == 302

    history = [item for item in requests_mock.request_history if countersign_advice_url in item.url]
    assert len(history) == 1
    history = history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": "b32d7dfa-a90d-4b37-adac-db231d4b83be",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason0",
        },
        {
            "id": "c9a96d84-6a6b-421d-bbbb-b12b9577d46e",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason0",
        },
    ]
