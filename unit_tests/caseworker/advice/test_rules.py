from unittest import mock

import pytest
import rules

from django.http import HttpRequest

from caseworker.advice import rules as advice_rules
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
def data_assigned_case(data_standard_case):
    case = Case(data_standard_case["case"])
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


def test_can_user_make_recommendation_request_missing_attributes(mock_gov_user, data_fake_queue, data_standard_case):
    case = Case(data_standard_case["case"])
    request = None

    assert not advice_rules.can_user_make_recommendation(request, case)


def test_can_user_make_recommendation_user_not_allocated(mock_gov_user, data_fake_queue, data_standard_case):
    case = Case(data_standard_case["case"])
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)

    assert not rules.test_rule("can_user_make_recommendation", request, case)


@mock.patch("caseworker.advice.rules.services.get_my_advice")
def test_can_user_make_recommendation_user_allocated_existing_advice(
    mock_get_my_advice, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_get_my_advice.return_value = True
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


@pytest.mark.parametrize(
    "queue_alias",
    (
        services.FCDO_CASES_TO_REVIEW_QUEUE,
        services.FCDO_CPACC_CASES_TO_REVIEW_QUEUE,
    ),
)
def test_can_user_make_recommendation_user_allocated_fcdo_allow(
    queue_alias, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.FCDO_TEAM
    data_fake_queue["alias"] = queue_alias
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_make_recommendation_user_allocated_fcdo_queue_mismatch(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.FCDO_TEAM
    data_fake_queue["alias"] = "some_queue"
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


@mock.patch("caseworker.advice.rules.services.unadvised_countries")
def test_can_user_make_recommendation_user_allocated_fcdo_all_countries_advised(
    mock_unadvised_countries, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_unadvised_countries.return_value = [1, 2]
    mock_gov_user["user"]["team"]["alias"] = services.FCDO_TEAM
    data_fake_queue["alias"] = services.FCDO_CASES_TO_REVIEW_QUEUE
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


@pytest.mark.parametrize(
    "queue_alias",
    services.MOD_CONSOLIDATE_QUEUES,
)
def test_can_user_make_recommendation_user_allocated_mod_allow(
    queue_alias, mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.MOD_CONSOLIDATE_TEAMS[0]
    data_fake_queue["alias"] = queue_alias
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_make_recommendation_user_allocated_mod_queue_mismatch(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.MOD_CONSOLIDATE_TEAMS[0]
    data_fake_queue["alias"] = "some-mismatched-queue"
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_make_recommendation_user_allocated_desnz_chemical_allow(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.DESNZ_TEAMS[0]
    data_fake_queue["alias"] = services.DESNZ_CHEMICAL_CASES_TO_REVIEW
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_make_recommendation_user_allocated_desnz_queue_mismatch(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.DESNZ_TEAMS[0]
    data_fake_queue["alias"] = "some-mismatched-queue"
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


@pytest.mark.parametrize(
    "unassessed_trigger_list_goods_result, expected_permission_result",
    (
        ([], True),
        ([1], False),
    ),
)
@mock.patch("caseworker.advice.rules.services.unassessed_trigger_list_goods")
def test_can_user_make_recommendation_user_allocated_desnz_nuclear_trigger_list_goods(
    mock_unassessed_trigger_list_goods,
    unassessed_trigger_list_goods_result,
    expected_permission_result,
    mock_gov_user,
    data_fake_queue,
    data_assigned_case,
):
    mock_unassessed_trigger_list_goods.return_value = unassessed_trigger_list_goods_result
    mock_gov_user["user"]["team"]["alias"] = services.DESNZ_TEAMS[0]
    data_fake_queue["alias"] = services.DESNZ_NUCLEAR_CASES_TO_REVIEW
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case) == expected_permission_result


def test_can_user_make_recommendation_user_allocated_ncsc_allow(mock_gov_user, data_fake_queue, data_assigned_case):
    mock_gov_user["user"]["team"]["alias"] = services.NCSC_TEAM
    data_fake_queue["alias"] = services.NCSC_CASES_TO_REVIEW
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_make_recommendation_user_allocated_ncsc_queue_mismatch(
    mock_gov_user, data_fake_queue, data_assigned_case
):
    mock_gov_user["user"]["team"]["alias"] = services.NCSC_TEAM
    data_fake_queue["alias"] = "mismatched-queue"
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert not rules.test_rule("can_user_make_recommendation", request, data_assigned_case)


def test_can_user_allocate_and_approve(mock_gov_user, data_fake_queue, data_standard_case):
    # User satisfies `can_user_allocate_and_approve` criteria, but is not yet allocated
    case = Case(data_standard_case["case"])
    mock_gov_user["user"]["team"]["alias"] = services.NCSC_TEAM
    data_fake_queue["alias"] = services.NCSC_CASES_TO_REVIEW
    request = get_mock_request(mock_gov_user["user"], data_fake_queue)
    assert rules.test_rule("can_user_allocate_and_approve", request, case)
