import pytest
import requests
import rules

from itertools import chain
from unittest import mock

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
    # Must be added as client requests assume RequestsSessionMiddleware has run
    request.requests_session = requests.Session()
    request.session = {}
    return request


def get_allocated_request_user(user, queue, team=None):
    if team:
        user["user"]["team"] = team
    request = get_mock_request(user["user"], queue)
    return request


class TestIsUserAllowedToMakeRecommendationRule:

    def test_request_missing_attributes(self, data_unassigned_case):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.is_user_allowed_to_make_f680_recommendation(request, case)

    @pytest.mark.parametrize(
        "case_status, expected",
        (
            chain(
                ((status, False) for status in recommendation_rules.INFORMATIONAL_STATUSES),
                ((status, True) for status in recommendation_rules.RECOMMENDATION_STATUSES),
                ((status, True) for status in recommendation_rules.OUTCOME_STATUSES),
            )
        ),
    )
    def test_user_allowed_to_make_f680_recommendation(
        self, mock_gov_user, data_fake_queue, data_assigned_case, case_status, expected
    ):
        team = {"id": MOD_ECJU, "alias": services.MOD_ECJU_TEAM}
        data_assigned_case.data["status"]["key"] = case_status
        request = get_allocated_request_user(mock_gov_user, data_fake_queue, team=team)

        assert rules.test_rule("is_user_allowed_to_make_f680_recommendation", request, data_assigned_case) is expected


class TestCanUserMakeF680RecommendationRule:

    def test_can_user_make_f680_recommendation_request_missing_attributes(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.can_user_make_f680_recommendation(request, case)

    def test_can_user_make_f680_recommendation_user_not_allocated(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_recommendation", request, case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_with_existing_recommendation_no_pending(
        self,
        mock_get_pending_recommendations,
        mock_get_my_recommendation,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_pending_recommendations.return_value = False
        mock_get_my_recommendation.return_value = True
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)
        assert not rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_with_existing_recommendation_and_pending(
        self,
        mock_get_pending_recommendations,
        mock_get_my_recommendation,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_pending_recommendations.return_value = True
        mock_get_my_recommendation.return_value = True
        data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)
        assert rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_can_user_make_f680_recommendation_user_allocated_incorrect_case_status(
        self,
        mock_get_pending_recommendations,
        mock_get_my_recommendation,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_pending_recommendations.return_value = True
        mock_get_my_recommendation.return_value = True
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)
        assert not rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_can_user_make_f680_recommendation_user_allocated(
        self,
        mock_get_pending_recommendations,
        mock_get_my_recommendation,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_my_recommendation.return_value = False
        mock_get_pending_recommendations.return_value = True
        data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE

        request = get_allocated_request_user(mock_gov_user, data_fake_queue)
        assert rules.test_rule("can_user_make_f680_recommendation", request, data_assigned_case)


class TestCanUserMoveF680CaseForwardRule:

    def test_can_user_move_f680_case_forward_request_missing_attributes(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.f680_case_ready_for_move(request, case)

    def test_can_user_move_f680_case_forward_user_not_allocated_denied(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)

        assert not rules.test_rule("can_user_move_f680_case_forward", request, case)

    def test_can_user_move_f680_case_forward_user_allocated_wrong_status_denied(
        self, mock_gov_user, data_fake_queue, data_assigned_case
    ):
        case = data_assigned_case
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW

        assert not rules.test_rule("can_user_move_f680_case_forward", request, case)

    def test_can_user_move_f680_case_forward_informational_status_granted(
        self, mock_gov_user, data_fake_queue, data_assigned_case
    ):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.SUBMITTED
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert rules.test_rule("can_user_move_f680_case_forward", request, case)

    @mock.patch("caseworker.f680.rules.get_case_recommendations")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_can_user_move_f680_case_forward_recommendation_status_no_recommendation_denied(
        self,
        mock_get_pending_recommendations,
        mock_case_recommendations,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_pending_recommendations.return_value = False
        mock_case_recommendations.return_value = []
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
    @mock.patch("caseworker.f680.rules.get_case_recommendations")
    @mock.patch("caseworker.f680.rules.get_pending_recommendation_requests")
    def test_can_user_move_f680_case_forward_recommendation_status_granted(
        self,
        mock_get_pending_recommendations,
        mock_case_recommendations,
        team,
        mock_gov_user,
        data_fake_queue,
        data_assigned_case,
    ):
        mock_get_pending_recommendations.return_value = False
        mock_case_recommendations.return_value = [{"type": "approve", "team": team}]
        case = data_assigned_case
        data_assigned_case.data["status"]["key"] = CaseStatusEnum.OGD_ADVICE
        request = get_allocated_request_user(mock_gov_user, data_fake_queue, team=team)

        assert rules.test_rule("can_user_move_f680_case_forward", request, case)


class TestCanUserMakeF680OutcomeRule:
    def test_can_user_make_f680_outcome_user_not_allocated(self, mock_gov_user, data_fake_queue, data_unassigned_case):
        case = data_unassigned_case
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_outcome", request, case)

    def test_can_user_make_f680_outcome_user_allocated_wrong_status(
        self, mock_gov_user, data_fake_queue, data_assigned_case
    ):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.SUBMITTED
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_outcome", request, case)

    def test_can_user_make_f680_outcome_permission_granted(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_no_outcome
    ):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert rules.test_rule("can_user_make_f680_outcome", request, case)

    def test_can_user_make_f680_outcome_existing_outcome_denied(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete
    ):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_outcome", request, case)

    def test_case_ready_for_outcome_request_missing_attributes(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.case_ready_for_outcome(request, case)

    def test_releases_without_outcome_request_missing_attributes(
        self, mock_gov_user, data_fake_queue, data_unassigned_case
    ):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.releases_without_outcome(request, case)


class TestClearF680RecommendationRule:

    def test_request_missing_attributes(self, mock_gov_user, data_fake_queue, data_unassigned_case):
        case = data_unassigned_case
        request = None

        assert not recommendation_rules.can_user_clear_f680_recommendation(request, case)

    def test_user_not_allocated(self, mock_gov_user, data_fake_queue, data_unassigned_case):
        case = data_unassigned_case
        request = get_mock_request(mock_gov_user["user"], data_fake_queue)

        assert not rules.test_rule("can_user_clear_f680_recommendation", request, case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    def test_with_no_user_recommendations(
        self, mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
    ):
        mock_get_my_recommendation.return_value = []
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)
        assert not rules.test_rule("can_user_clear_f680_recommendation", request, data_assigned_case)

    @mock.patch("caseworker.f680.rules.recommendations_by_current_user")
    def test_with_user_recommendations(
        self, mock_get_my_recommendation, mock_gov_user, data_fake_queue, data_assigned_case
    ):
        mock_get_my_recommendation.return_value = [{"type": "approve"}, {"type": "refuse"}]
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)
        assert rules.test_rule("can_user_clear_f680_recommendation", request, data_assigned_case)


class TestCanUserMakeF680LetterRule:
        
    def test_can_user_make_f680_outcome_letter_granted(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert rules.test_rule("can_user_make_f680_outcome_letter", request, case)

    def test_can_user_make_f680_outcome_letter_wrong_status(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.FINALISED
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_outcome_letter", request, case)

    
    def test_can_user_make_f680_outcome_letter_wrong_out_come_not_decided(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_no_outcome):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_f680_outcome_letter", request, case)

    
    def test_can_user_make_f680_outcome_approval_letter_granted(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete_approval):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert rules.test_rule("can_user_make_approval_f680_outcome_letter", request, case)

    def test_can_user_make_f680_outcome_approval_letter_not_allowed(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete_refusal):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_approval_f680_outcome_letter", request, case)

    def test_can_user_make_f680_outcome_refusal_letter_granted(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete_refusal):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert rules.test_rule("can_user_make_refusal_f680_outcome_letter", request, case)

    def test_can_user_make_f680_outcome_refusal_letter_not_allowed(
        self, mock_gov_user, data_fake_queue, data_assigned_case, mock_outcomes_complete_approval):
        case = data_assigned_case
        case.data["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        request = get_allocated_request_user(mock_gov_user, data_fake_queue)

        assert not rules.test_rule("can_user_make_refusal_f680_outcome_letter", request, case)