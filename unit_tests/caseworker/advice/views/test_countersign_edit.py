from unittest.mock import patch
from uuid import uuid4
import pytest
from bs4 import BeautifulSoup

from caseworker.advice import services
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


@pytest.fixture
def countersign_decision_edit_url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_decision_edit",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def countersign_advice(data_standard_case, advice_for_countersign, current_user):
    return [
        {
            "id": str(uuid4()),
            "valid": True,
            "order": services.FIRST_COUNTERSIGN,
            "outcome_accepted": True,
            "reasons": "I concur",
            "countersigned_user": current_user,
            "case": data_standard_case["case"]["id"],
            "advice": item,
        }
        for item in advice_for_countersign
    ]


def test_countersign_edit_trigger_list_products(
    authorized_client, requests_mock, data_standard_case_with_all_trigger_list_products_assessed, url
):
    case_id = data_standard_case_with_all_trigger_list_products_assessed["case"]["id"]
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case_with_all_trigger_list_products_assessed
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    expected_context = [
        {"line_number": num, **good}
        for num, good in enumerate(
            data_standard_case_with_all_trigger_list_products_assessed["case"]["data"]["goods"], start=1
        )
    ]
    assert response.context["assessed_trigger_list_goods"] == expected_context


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


def test_lu_countersign_decision_edit_post_form_errors(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    current_user,
    countersign_advice,
    countersign_decision_edit_url,
):
    case_id = standard_case_with_advice["id"]
    queue_details = {
        "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
        "name": "Licensing manager",
        "alias": services.LU_LICENSING_MANAGER_QUEUE,
    }
    # Set up advice on the case
    data_standard_case["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    data_standard_case["case"]["queue_details"] = [queue_details]
    data_standard_case["case"]["advice"] = advice_for_countersign
    data_standard_case["case"]["countersign_advice"] = countersign_advice
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM
    for item in advice_for_countersign:
        item["user"] = current_user
        item["level"] = "final"

    # Setup mock API requests
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)

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

    response = authorized_client.post(countersign_decision_edit_url, data=data)
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
def test_lu_countersign_decision_edit_post_success(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    current_user,
    countersign_advice,
    countersign_decision_edit_url,
    queue_details,
    outcome_accepted,
):
    case_id = data_standard_case["case"]["id"]
    user_id = current_user["id"]

    # Set up advice on the case
    data_standard_case["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    data_standard_case["case"]["queue_details"] = [queue_details]
    data_standard_case["case"]["advice"] = advice_for_countersign
    data_standard_case["case"]["countersign_advice"] = countersign_advice
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM
    for item in advice_for_countersign:
        item["user"] = current_user
        item["level"] = "final"
    # Setup mock API requests
    countersign_advice_url = client._build_absolute_uri(f"/cases/{case_id}/countersign-decision-advice/")
    requests_mock.put(countersign_advice_url, json={})
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

    response = authorized_client.post(countersign_decision_edit_url, data=data)

    assert response.status_code == 302
    history = [item for item in requests_mock.request_history if countersign_advice_url in item.url]
    assert len(history) == 1
    history = history.pop()
    assert history.method == "PUT"
    assert history.json() == [
        {
            "id": countersign_advice[0]["id"],
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
        },
        {
            "id": countersign_advice[1]["id"],
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
        },
        {
            "id": countersign_advice[2]["id"],
            "outcome_accepted": outcome_accepted,
            "reasons": "reason0",
        },
    ]


@patch("caseworker.advice.views.mixins.get_gov_user")
def test_lu_countersign_edit_get_shows_previous_countersignature(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    current_user,
    countersign_advice,
    countersign_decision_edit_url,
):
    case_id = standard_case_with_advice["id"]
    queue_details = {
        "id": "566fd526-bd6d-40c1-94bd-60d10c961234",
        "name": "Licensing manager",
        "alias": services.LU_LICENSING_MANAGER_QUEUE,
    }
    # Set up advice on the case
    data_standard_case["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    data_standard_case["case"]["queue_details"] = [queue_details]
    data_standard_case["case"]["advice"] = advice_for_countersign
    data_standard_case["case"]["countersign_advice"] = countersign_advice
    current_user["team"]["alias"] = services.LICENSING_UNIT_TEAM
    for item in advice_for_countersign:
        item["user"] = current_user
        item["level"] = "final"
    # Setup mock API requests
    team_id = current_user["team"]["id"]
    mock_get_gov_user.return_value = (
        {"user": current_user},
        None,
    )

    response = authorized_client.get(countersign_decision_edit_url)
    soup = BeautifulSoup(response.content, "html.parser")
    countersignature_block = soup.find(class_="countersignatures")
    assert response.status_code == 200

    counter_sigs = countersignature_block.find_all("div", recursive=False)
    assert len(counter_sigs) == 1
    assert (
        counter_sigs[0].find(class_="govuk-heading-m").text
        == f"Countersigned by {current_user['first_name']} {current_user['last_name']}"
    )
    assert counter_sigs[0].find(class_="govuk-body").text == "I concur"
    assert "True" == soup.find(id="id_form-0-outcome_accepted_0")["value"]
    assert "I concur" in soup.find(id="id_form-0-approval_reasons").text
