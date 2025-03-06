from unittest import mock

import pytest
import rules

from django.http import HttpRequest

from caseworker.f680 import rules as recommendation_rules
from caseworker.advice import services
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
def data_assigned_case(data_submitted_f680_case):
    case = Case(data_submitted_f680_case["case"])
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


def test_can_user_make_f680_recommendation_request_missing_attributes(
    mock_gov_user, data_fake_queue, data_submitted_f680_case
):
    case = Case(data_submitted_f680_case["case"])
    request = None

    assert not recommendation_rules.can_user_make_f680_recommendation(request, case)


def test_can_user_make_f680_recommendation_user_not_allocated(mock_gov_user, data_fake_queue, data_submitted_f680_case):
    case = Case(data_submitted_f680_case["case"])
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)

    assert not rules.test_rule("can_user_make_f680_recommendation", request, case)


@mock.patch("caseworker.f680.rules.current_user_recommendation")
def test_can_user_make_f680_recommendation_user_allocated_existing_recommendation(
    mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_get_my_recommendation.return_value = True
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)


@pytest.mark.parametrize(
    "queue_alias",
    (
        services.MOD_CAPPROT_TEAM,
        services.MOD_DSR_TEAM,
    ),
)
def test_can_user_make_f680_recommendation_user_allocated(
    queue_alias, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = queue_alias
    data_fake_queue["alias"] = queue_alias
    data_assigned_case['data']['status'] = {'key': 'ogd_advice', 'value': 'OGD Advice'}
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)
