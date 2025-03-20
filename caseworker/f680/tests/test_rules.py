from unittest import mock

import pytest
import rules

from django.http import HttpRequest

from core.constants import CaseStatusEnum

from caseworker.f680 import rules as recommendation_rules
from caseworker.advice import services
from caseworker.advice.constants import MOD_CAPPROT_TEAM, MOD_DSR_TEAM, MOD_ECJU
from caseworker.cases.objects import Case


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"  # /PS-IGNORE


@pytest.fixture
def data_fake_queue():
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "alias": "fake",
        "name": "Fake queue",
        "is_system_queue": False,
        "countersigning_queue": None,
    }


@pytest.fixture
def data_unassigned_case(data_submitted_f680_case):
    case = Case(data_submitted_f680_case["case"])
    return case


@pytest.fixture
def data_assigned_case(data_unassigned_case):
    case = data_unassigned_case
    case.assigned_users = {
        "fake queue": [
            {"id": mock_gov_user_id},
        ]
    }
    return case


def get_mock_request(user, queue):
    request = HttpRequest()
    request.lite_user = user
    request.queue = queue
    return request


def get_allocated_request_user(user, queue, team=None):
    if team:
        user["user"]["team"] = team
    request = get_mock_request(user["user"], queue)
    return request


def test_can_user_make_f680_recommendation_request_missing_attributes(
    mock_gov_user, data_fake_queue, data_unassigned_case
):
    case = data_unassigned_case
    request = None

    assert not recommendation_rules.can_user_make_f680_recommendation(request, case)


def test_can_user_make_f680_recommendation_user_not_allocated(mock_gov_user, data_fake_queue, data_unassigned_case):
    case = data_unassigned_case
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)

    assert not rules.test_rule("can_user_make_f680_recommendation", request, case)


@mock.patch("caseworker.f680.rules.current_user_recommendations")
def test_can_user_make_f680_recommendation_user_allocated_existing_recommendation(
    mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_get_my_recommendation.return_value = True
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)


@mock.patch("caseworker.f680.rules.current_user_recommendations")
def test_can_user_make_f680_recommendation_user_allocated_incorrect_case_status(
    mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_get_my_recommendation.return_value = True
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)
    assert not rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)


@mock.patch("caseworker.f680.rules.current_user_recommendations")
def test_can_user_make_f680_recommendation_user_allocated(
    mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_get_my_recommendation.return_value = False
    data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE

    request = get_allocated_request_user(mock_gov_user, data_fake_queue)
    assert rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)


def test_can_user_move_f680_case_forward_request_missing_attributes(
    mock_gov_user, data_fake_queue, data_unassigned_case
):
    case = data_unassigned_case
    request = None

    assert not recommendation_rules.f680_case_ready_for_move(request, case)


def test_can_user_move_f680_case_forward_user_not_allocated_denied(
    mock_gov_user, data_fake_queue, data_unassigned_case
):
    case = data_unassigned_case
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)

    assert not rules.test_rule("can_user_move_f680_case_forward", request, case)


def test_can_user_move_f680_case_forward_user_allocated_wrong_status_denied(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    case = data_assigned_case
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)
    case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW

    assert not rules.test_rule("can_user_move_f680_case_forward", request, case)


def test_can_user_move_f680_case_forward_informational_status_granted(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    case = data_assigned_case
    case.data["status"]["key"] = CaseStatusEnum.SUBMITTED
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)

    assert rules.test_rule("can_user_move_f680_case_forward", request, case)


def test_can_user_move_f680_case_forward_recommendation_status_no_recommendation_denied(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    case = data_assigned_case
    data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)

    assert not rules.test_rule("can_user_move_f680_case_forward", request, case)


@pytest.mark.parametrize(
    "team",
    (
        {"id": MOD_CAPPROT_TEAM, "alias": services.MOD_CAPPROT_TEAM},
        {"id": MOD_DSR_TEAM, "alias": services.MOD_DSR_TEAM},
    ),
)
def test_can_user_move_f680_case_forward_recommendation_status_granted(
    team, mock_gov_user, data_fake_queue, data_assigned_case
):
    case = data_assigned_case
    case.advice = [{"team": team}]
    data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE
    request = get_allocated_request_user(mock_gov_user, data_fake_queue, team=team)

    assert rules.test_rule("can_user_move_f680_case_forward", request, case)


def test_can_user_move_f680_case_forward_recommendation_status_mod_ecju_granted(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    case = data_assigned_case
    team = {"id": MOD_ECJU, "alias": services.MOD_ECJU_TEAM}
    data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE
    request = get_allocated_request_user(mock_gov_user, data_fake_queue, team=team)

    assert rules.test_rule("can_user_move_f680_case_forward", request, case)


def test_can_user_make_f680_outcome_user_not_allocated(mock_gov_user, data_fake_queue, data_unassigned_case):
    case = data_unassigned_case
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)

    assert not rules.test_rule("can_user_make_f680_outcome", request, case)


def test_can_user_make_f680_outcome_user_allocated_wrong_status(mock_gov_user, data_fake_queue, data_assigned_case):
    case = data_assigned_case
    case.data["status"]["key"] = CaseStatusEnum.SUBMITTED
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)

    assert not rules.test_rule("can_user_make_f680_outcome", request, case)


def test_can_user_make_f680_outcome_permission_granted(mock_gov_user, data_fake_queue, data_assigned_case):
    case = data_assigned_case
    case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
    request = get_allocated_request_user(mock_gov_user, data_fake_queue)

    assert rules.test_rule("can_user_make_f680_outcome", request, case)


def test_can_user_make_f680_outcome_request_missing_attributes(mock_gov_user, data_fake_queue, data_unassigned_case):
    case = data_unassigned_case
    request = None

    assert not recommendation_rules.case_ready_for_outcome(request, case)
