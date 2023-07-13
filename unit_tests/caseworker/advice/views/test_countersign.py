from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM
from core import client
from caseworker.advice import services
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_picklist, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def countersign_decision_url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_decision_review",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
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
            "id": "825bddc9-4e6c-4a26-8231-9c0500b037a6",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason0",
        },
        {
            "id": "b32d7dfa-a90d-4b37-adac-db231d4b83be",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason1",
        },
        {
            "id": "c9a96d84-6a6b-421d-bbbb-b12b9577d46e",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason1",
        },
    ]


def test_lu_countersign_decision_post_form_errors(
    authorized_client,
    requests_mock,
    standard_case_with_advice,
    advice_for_countersign,
    current_user,
    countersign_decision_url,
):
    case_id = standard_case_with_advice["id"]

    # Set up advice on the case
    standard_case_with_advice["advice"] = advice_for_countersign
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM
    for item in advice_for_countersign:
        item["user"] = current_user
        item["level"] = "final"

    # Setup mock API requests
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=standard_case_with_advice)

    advice_to_countersign = services.get_advice_to_countersign(advice_for_countersign, current_user)

    data = {
        "form-TOTAL_FORMS": [f"{len(advice_to_countersign)}"],
        "form-INITIAL_FORMS": ["0"],
        "form-MIN_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "form-MAX_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "submit": ["Submit"],
    }

    for index, item in enumerate(advice_to_countersign.keys()):
        data[f"form-{index}-outcome_accepted"] = [True]
        data[f"form-{index}-approval_reasons"] = [""]
        requests_mock.get(client._build_absolute_uri(f"/users/{item}/team-queues/"), json={"queues": []})

    response = authorized_client.post(countersign_decision_url, data=data)
    assert response.status_code == 200
    assert response.context["formset"].errors == [{"approval_reasons": ["Enter a reason for countersigning"]}]


@pytest.mark.parametrize(
    "queue_details,outcome_accepted",
    (
        (
            {
                "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
                "name": "Licensing manager",
                "alias": services.LU_LICENSING_MANAGER_QUEUE,
            },
            True,
        ),
        (
            {
                "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
                "name": "Licensing manager",
                "alias": services.LU_LICENSING_MANAGER_QUEUE,
            },
            False,
        ),
        (
            {
                "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
                "name": "Senior licensing manager",
                "alias": services.LU_SR_LICENSING_MANAGER_QUEUE,
            },
            True,
        ),
        (
            {
                "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
                "name": "Senior licensing manager",
                "alias": services.LU_SR_LICENSING_MANAGER_QUEUE,
            },
            False,
        ),
    ),
)
def test_lu_countersign_decision_post_success(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    current_user,
    queue_details,
    outcome_accepted,
):
    case_id = data_standard_case["case"]["id"]
    user_id = current_user["id"]

    # Set up advice on the case
    data_standard_case["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    data_standard_case["case"]["queue_details"] = [queue_details]
    data_standard_case["case"]["advice"] = advice_for_countersign
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM
    for item in advice_for_countersign:
        item["user"] = current_user
        item["level"] = "final"

    # Setup mock API requests
    countersign_advice_url = client._build_absolute_uri(f"/cases/{case_id}/countersign-decision-advice/")
    requests_mock.post(countersign_advice_url, json={})
    case_url = reverse("cases:case", kwargs={"queue_pk": queue_details["id"], "pk": case_id})
    requests_mock.get(client._build_absolute_uri(case_url), json=data_standard_case)
    requests_mock.get(client._build_absolute_uri(f"/gov-users/{user_id}"), json={"user": current_user})

    advice_to_countersign = services.get_advice_to_countersign(advice_for_countersign, current_user)

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
        data[f"form-{index}-outcome_accepted"] = [outcome_accepted]
        data[f"form-{index}-approval_reasons"] = [f"reason{index}" if outcome_accepted else ""]
        data[f"form-{index}-rejected_reasons"] = [f"reason{index}" if not outcome_accepted else ""]
        requests_mock.get(client._build_absolute_uri(f"/users/{item}/team-queues/"), json={"queues": []})

    countersign_decision_url = reverse(
        f"cases:countersign_decision_review",
        kwargs={"queue_pk": queue_details["id"], "pk": case_id},
    )
    response = authorized_client.post(countersign_decision_url, data=data)
    assert response.status_code == 302

    expected_order = 2 if queue_details["alias"] == services.LU_SR_LICENSING_MANAGER_QUEUE else 1
    history = [item for item in requests_mock.request_history if countersign_advice_url in item.url]
    assert len(history) == 1
    history = history.pop()
    assert history.method == "POST"
    assert history.json() == [
        {
            "order": expected_order,
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
            "countersigned_user": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "case": "8fb76bed-fd45-4293-95b8-eda9468aa254",
            "advice": "825bddc9-4e6c-4a26-8231-9c0500b037a6",
        },
        {
            "order": expected_order,
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
            "countersigned_user": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "case": "8fb76bed-fd45-4293-95b8-eda9468aa254",
            "advice": "b32d7dfa-a90d-4b37-adac-db231d4b83be",
        },
        {
            "order": expected_order,
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
            "countersigned_user": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "case": "8fb76bed-fd45-4293-95b8-eda9468aa254",
            "advice": "c9a96d84-6a6b-421d-bbbb-b12b9577d46e",
        },
    ]


@patch("caseworker.advice.views.get_gov_user")
def test_lu_countersign_get_shows_previous_countersignature(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    standard_case_with_advice,
    current_user,
    final_advice,
):
    case_id = data_standard_case["case"]["id"]

    queue_details = {
        "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
        "name": "Senior licensing manager",
        "alias": services.LU_SR_LICENSING_MANAGER_QUEUE,
    }
    # Set up advice on the case
    team_id = final_advice["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = [final_advice]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        [final_advice], [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True}]
    )
    # Setup mock API requests
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )

    countersign_decision_url = reverse(
        f"cases:countersign_decision_review",
        kwargs={"queue_pk": queue_details["id"], "pk": case_id},
    )
    response = authorized_client.get(countersign_decision_url)
    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(class_="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 1
    assert counter_sigs[0].find(class_="govuk-heading-m").text == "Countersigned by Testy McTest"
    assert counter_sigs[0].find(class_="govuk-body").text == "I concur"
