import pytest

from bs4 import BeautifulSoup
from unittest.mock import patch
from uuid import uuid4

from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM
from core import client
from caseworker.advice import services
from caseworker.advice.constants import AdviceLevel, AdviceType
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_denial_reasons,
    mock_case,
    mock_gov_lu_case_officer,
    mock_gov_lu_licensing_manager,
    mock_gov_lu_senior_licensing_manager,
):
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


@pytest.fixture
def countersign_advice_view_url(data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_advice_view",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def ogd_advice(FCDO_team_user, fcdo_team, MOD_team1_user, MOD_team1):
    return [
        {
            "created_at": "2021-07-14T15:20:35.713348+01:00",
            "countersigned_by": None,
            "end_user": None,
            "footnote": None,
            "good": str(uuid4()),
            "id": str(uuid4()),
            "level": AdviceLevel.USER,
            "note": "",
            "proviso": None,
            "text": "",
            "type": {"key": AdviceType.APPROVE, "value": AdviceType.APPROVE},
            "user": FCDO_team_user,
            "team": fcdo_team,
        },
        {
            "created_at": "2021-07-14T15:20:35.713348+01:00",
            "countersigned_by": None,
            "end_user": None,
            "footnote": None,
            "good": str(uuid4()),
            "id": str(uuid4()),
            "level": AdviceLevel.USER,
            "note": "",
            "proviso": None,
            "text": "",
            "type": {"key": AdviceType.APPROVE, "value": AdviceType.APPROVE},
            "user": MOD_team1_user,
            "team": MOD_team1,
        },
    ]


@pytest.fixture
def final_level_advice(LU_case_officer):
    return [
        {
            "id": str(uuid4()),
            "good": str(uuid4()),
            "created_at": "2021-07-14T15:20:35.713348+01:00",
            "countersigned_by": None,
            "footnote": None,
            "level": AdviceLevel.FINAL,
            "note": "",
            "proviso": None,
            "text": "issue",
            "type": {"key": AdviceType.APPROVE, "value": AdviceType.APPROVE},
            "user": LU_case_officer,
            "team": LU_case_officer["team"],
        }
        for _ in range(2)
    ]


@pytest.fixture
def licensing_manager_countersignature(LU_licensing_manager, final_level_advice):
    return [
        {
            "order": services.FIRST_COUNTERSIGN,
            "valid": True,
            "outcome_accepted": True,
            "reasons": "Agree with the decision to issue",
            "countersigned_user": LU_licensing_manager,
            "advice": advice,
        }
        for advice in final_level_advice
    ]


@pytest.fixture
def licensing_manager_queue():
    return {
        "id": "f458094c-1fed-4222-ac70-ff5fa20ff649",
        "name": "Licensing manager countersigning",
        "alias": services.LU_LICENSING_MANAGER_QUEUE,
    }


@pytest.fixture
def senior_licensing_manager_queue():
    return {
        "id": "a8078cbc-d94f-40b3-9adf-8a9f93f88d4e",
        "name": "Senior Licensing manager countersigning",
        "alias": services.LU_SR_LICENSING_MANAGER_QUEUE,
    }


@pytest.fixture
def case_licensing_manager_countersign_queue_url(data_standard_case, licensing_manager_queue):
    return reverse(
        f"cases:countersign_advice_view",
        kwargs={
            "queue_pk": licensing_manager_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def case_licensing_manager_countersign_decision_url(data_standard_case, licensing_manager_queue):
    return reverse(
        f"cases:countersign_decision_review",
        kwargs={
            "queue_pk": licensing_manager_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def case_senior_licensing_manager_countersign_queue_url(data_standard_case, senior_licensing_manager_queue):
    return reverse(
        f"cases:countersign_advice_view",
        kwargs={
            "queue_pk": senior_licensing_manager_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def case_senior_licensing_manager_countersign_decision_url(data_standard_case, senior_licensing_manager_queue):
    return reverse(
        f"cases:countersign_decision_review",
        kwargs={
            "queue_pk": senior_licensing_manager_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def licensing_manager_countersigning_case(
    data_standard_case, licensing_manager_queue, ogd_advice, final_level_advice, LU_case_officer
):
    data_standard_case["case"]["advice"] = ogd_advice
    data_standard_case["case"]["advice"].extend(final_level_advice)
    data_standard_case["case"]["queue_details"] = [licensing_manager_queue]
    data_standard_case["case"]["case_officer"] = LU_case_officer

    return data_standard_case


@pytest.fixture
def licensing_manager_countersigning_case_assigned_to_user(licensing_manager_countersigning_case, LU_licensing_manager):
    licensing_manager_countersigning_case["case"]["assigned_users"] = {
        "LU countersigning": [LU_licensing_manager],
    }

    return licensing_manager_countersigning_case


@pytest.fixture
def senior_licensing_manager_countersigning_case(
    senior_licensing_manager_queue,
    licensing_manager_countersignature,
    licensing_manager_countersigning_case,
):
    licensing_manager_countersigning_case["case"]["countersign_advice"] = licensing_manager_countersignature
    licensing_manager_countersigning_case["case"]["queue_details"] = [senior_licensing_manager_queue]

    return licensing_manager_countersigning_case


@pytest.fixture
def senior_licensing_manager_countersigning_case_assigned_to_licensing_manager(
    senior_licensing_manager_countersigning_case, LU_licensing_manager
):
    senior_licensing_manager_countersigning_case["case"]["assigned_users"] = {
        "LU senior manager countersigning": [LU_licensing_manager],
    }

    return senior_licensing_manager_countersigning_case


@pytest.fixture
def senior_licensing_manager_countersigning_case_assigned_to_user(
    senior_licensing_manager_countersigning_case, LU_senior_licensing_manager
):
    senior_licensing_manager_countersigning_case["case"]["assigned_users"] = {
        "LU countersigning": [LU_senior_licensing_manager],
    }

    return senior_licensing_manager_countersigning_case


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


# Licensing manager tests
def user_not_allowed_to_countersign(response):
    soup = BeautifulSoup(response.content, "html.parser")
    countersign_button = soup.find("a", {"id": "review-and-countersign-decision-button"})
    assert countersign_button is None

    message = soup.find("div", {"id": "lu-user-not-allowed-to-countersign"})
    assert message
    assert "You cannot countersign this case because you were the officer that assessed it." in message.text
    return True


@patch("caseworker.advice.views.get_gov_user")
@patch("caseworker.core.rules.get_logged_in_caseworker")
def test_case_officer_cannot_countersign_as_licensing_manager(
    mock_caseworker,
    mock_get_gov_user,
    case_licensing_manager_countersign_queue_url,
    authorized_client,
    LU_case_officer,
    licensing_manager_countersigning_case,
):
    """
    Licensing unit case officer is the one that gives final advice so
    test that the same user cannot countersign as licensing manager
    """
    mock_get_gov_user.return_value = ({"user": LU_case_officer}, None)
    mock_caseworker.return_value = LU_case_officer

    response = authorized_client.get(case_licensing_manager_countersign_queue_url)
    assert response.status_code == 200

    assert user_not_allowed_to_countersign(response)


@patch("caseworker.advice.views.get_gov_user")
@patch("caseworker.core.rules.get_logged_in_caseworker")
def test_licensing_manager_countersigner_not_same_as_case_officer(
    mock_caseworker,
    mock_get_gov_user,
    authorized_client,
    case_licensing_manager_countersign_queue_url,
    case_licensing_manager_countersign_decision_url,
    LU_licensing_manager,
    licensing_manager_countersigning_case_assigned_to_user,
):
    """
    Licensing manager countersigner should not be the same as case officer
    who gives final recommendation, this test ensures they are not the same users
    """
    mock_get_gov_user.return_value = ({"user": LU_licensing_manager}, None)
    mock_caseworker.return_value = LU_licensing_manager

    response = authorized_client.get(case_licensing_manager_countersign_queue_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    countersign_button = soup.find("a", {"id": "review-and-countersign-decision-button"})
    assert countersign_button
    assert countersign_button.text == "Review and countersign"
    assert countersign_button["href"] == case_licensing_manager_countersign_decision_url


# Senior Licensing manager tests
@patch("caseworker.advice.views.get_gov_user")
@patch("caseworker.core.rules.get_logged_in_caseworker")
def test_case_officer_cannot_countersign_as_senior_licensing_manager(
    mock_caseworker,
    mock_get_gov_user,
    case_senior_licensing_manager_countersign_queue_url,
    authorized_client,
    LU_case_officer,
    senior_licensing_manager_countersigning_case,
):
    """
    Licensing unit case officer is the one that gives final advice so
    test that the same user cannot countersign as senior licensing manager
    """
    mock_get_gov_user.return_value = ({"user": LU_case_officer}, None)
    mock_caseworker.return_value = LU_case_officer

    response = authorized_client.get(case_senior_licensing_manager_countersign_queue_url)
    assert response.status_code == 200

    assert user_not_allowed_to_countersign(response)


@patch("caseworker.advice.views.get_gov_user")
@patch("caseworker.core.rules.get_logged_in_caseworker")
def test_licensing_manager_cannot_countersign_as_senior_licensing_manager(
    mock_caseworker,
    mock_get_gov_user,
    case_senior_licensing_manager_countersign_queue_url,
    authorized_client,
    LU_licensing_manager,
    senior_licensing_manager_countersigning_case_assigned_to_licensing_manager,
):
    """
    Licensing unit case officer is the one that gives final advice so
    test that the same user cannot countersign as senior licensing manager
    """
    mock_get_gov_user.return_value = ({"user": LU_licensing_manager}, None)
    mock_caseworker.return_value = LU_licensing_manager

    response = authorized_client.get(case_senior_licensing_manager_countersign_queue_url)
    assert response.status_code == 200

    assert user_not_allowed_to_countersign(response)


@patch("caseworker.advice.views.get_gov_user")
@patch("caseworker.core.rules.get_logged_in_caseworker")
def test_senior_manager_countersigner_not_same_as_case_officer_or_countersigner(
    mock_caseworker,
    mock_get_gov_user,
    authorized_client,
    case_senior_licensing_manager_countersign_queue_url,
    case_senior_licensing_manager_countersign_decision_url,
    LU_senior_licensing_manager,
    senior_licensing_manager_countersigning_case_assigned_to_user,
):
    """
    Licensing manager countersigner should not be the same as case officer
    who gives final recommendation or the licensing manager countersigner,
    this test ensures they are not the same users
    """
    mock_get_gov_user.return_value = ({"user": LU_senior_licensing_manager}, None)
    mock_caseworker.return_value = LU_senior_licensing_manager

    response = authorized_client.get(case_senior_licensing_manager_countersign_queue_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    countersign_button = soup.find("a", {"id": "review-and-countersign-decision-button"})
    assert countersign_button
    assert countersign_button.text == "Review and countersign"
    assert countersign_button["href"] == case_senior_licensing_manager_countersign_decision_url


def test_countersign_advice_view_trigger_list_products(
    authorized_client,
    requests_mock,
    data_standard_case_with_all_trigger_list_products_assessed,
    countersign_advice_view_url,
):
    case_id = data_standard_case_with_all_trigger_list_products_assessed["case"]["id"]
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case_with_all_trigger_list_products_assessed
    )
    response = authorized_client.get(countersign_advice_view_url)
    assert response.status_code == 200
    expected_context = [
        {"line_number": num, **good}
        for num, good in enumerate(
            data_standard_case_with_all_trigger_list_products_assessed["case"]["data"]["goods"], start=1
        )
    ]
    assert response.context["assessed_trigger_list_goods"] == expected_context
