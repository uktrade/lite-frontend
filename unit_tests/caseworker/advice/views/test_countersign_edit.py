import pytest

from copy import deepcopy
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_edit", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_edit_post(authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url):
    case_data = data_standard_case
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]
    for advice in case_data["case"]["advice"]:
        advice["countersign_comments"] = "test"

    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{case_id}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )
    countersign_advice_url = client._build_absolute_uri(f"/cases/{case_id}/countersign-advice/")
    requests_mock.put(countersign_advice_url, json={})

    response = authorized_client.get(url)
    assert all([form.initial == {"approval_reasons": "test"} for form in response.context["formset"]])

    # Fill up the formset - starting with management form
    num_advice = len(case_data["case"]["advice"])
    data = {
        "form-TOTAL_FORMS": [f"{num_advice}"],
        "form-INITIAL_FORMS": ["0"],
        "form-MIN_NUM_FORMS": [f"{num_advice}"],
        "form-MAX_NUM_FORMS": [f"{num_advice}"],
        "submit": ["Submit"],
    }
    for index, item in enumerate(advice):
        data[f"form-{index}-approval_reasons"] = [f"test2"]

    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = [item for item in requests_mock.request_history if countersign_advice_url in item.url]
    assert len(history) == 1
    history = history[0]
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "test2",
        }
    ]
