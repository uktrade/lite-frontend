import rules

from core.constants import CaseStatusEnum
from core.decorators import with_logged_in_caseworker

from caseworker.core.rules import is_user_allocated
from caseworker.f680.outcome.constants import OutcomeType
from caseworker.f680.recommendation.services import (
    recommendations_by_current_user,
    filter_recommendation_by_team,
    get_case_recommendations,
    get_pending_recommendation_requests,
)
from caseworker.f680.outcome.services import (
    get_outcomes,
    get_releases_with_no_outcome,
)


RECOMMENDATION_STATUSES = [CaseStatusEnum.OGD_ADVICE]
OUTCOME_STATUSES = [CaseStatusEnum.UNDER_FINAL_REVIEW]
INFORMATIONAL_STATUSES = [CaseStatusEnum.SUBMITTED]


@rules.predicate
@with_logged_in_caseworker
def is_user_allowed_to_make_f680_recommendation(request, case):
    return case["data"]["status"]["key"] in RECOMMENDATION_STATUSES + OUTCOME_STATUSES


@rules.predicate
@with_logged_in_caseworker
def can_user_make_f680_recommendation(request, case):
    user = request.lite_user

    pending_recommendations = get_pending_recommendation_requests(request, case, user)
    if recommendations_by_current_user(request, case, user) and not pending_recommendations:
        return False

    return case["data"]["status"]["key"] in RECOMMENDATION_STATUSES


@rules.predicate
@with_logged_in_caseworker
def can_user_clear_f680_recommendation(request, case):
    user = request.lite_user

    return bool(recommendations_by_current_user(request, case, user))


@rules.predicate
@with_logged_in_caseworker
def f680_case_ready_for_move(request, case):
    user = request.lite_user
    case_status = case["data"]["status"]["key"]

    if case_status in INFORMATIONAL_STATUSES:
        return True

    if case_status in RECOMMENDATION_STATUSES:
        pending_recommendations = get_pending_recommendation_requests(request, case, user)
        if pending_recommendations:
            return False

        case_recommendations = get_case_recommendations(request, case)

        team = user["team"]
        team_recommendations_exist = bool(filter_recommendation_by_team(case_recommendations, team["id"]))
        if team_recommendations_exist:
            return True

    return False


@rules.predicate
@with_logged_in_caseworker
def case_ready_for_outcome(request, case):
    return case["data"]["status"]["key"] in OUTCOME_STATUSES


@rules.predicate
@with_logged_in_caseworker
def releases_without_outcome_exist(request, case):
    outcomes, _ = get_outcomes(request, case["id"])
    releases_without_outcome, _ = get_releases_with_no_outcome(request, outcomes, case)
    return len(releases_without_outcome) > 0


@rules.predicate
@with_logged_in_caseworker
def all_releases_decided(request, case):
    outcomes, _ = get_outcomes(request, case["id"])

    releases_without_outcome, _ = get_releases_with_no_outcome(request, outcomes, case)
    return len(releases_without_outcome) == 0


@rules.predicate
@with_logged_in_caseworker
def release_has_approval(request, case):
    outcomes, _ = get_outcomes(request, case["id"])
    return any(outcome["outcome"] == OutcomeType.APPROVE for outcome in outcomes)


@rules.predicate
@with_logged_in_caseworker
def release_has_refusal(request, case):
    outcomes, _ = get_outcomes(request, case["id"])
    return any(outcome["outcome"] == OutcomeType.REFUSE for outcome in outcomes)


rules.add_rule(
    "is_user_allowed_to_make_f680_recommendation", is_user_allocated & is_user_allowed_to_make_f680_recommendation
)
rules.add_rule("can_user_make_f680_recommendation", is_user_allocated & can_user_make_f680_recommendation)
rules.add_rule("can_user_clear_f680_recommendation", is_user_allocated & can_user_clear_f680_recommendation)
rules.add_rule(
    "can_user_make_f680_outcome", is_user_allocated & case_ready_for_outcome & releases_without_outcome_exist
)
rules.add_rule("can_user_move_f680_case_forward", is_user_allocated & f680_case_ready_for_move)
rules.add_rule("can_user_make_f680_outcome_letter", is_user_allocated & case_ready_for_outcome & all_releases_decided)
rules.add_rule(
    "can_user_make_approval_f680_outcome_letter",
    is_user_allocated & case_ready_for_outcome & all_releases_decided & release_has_approval,
)
rules.add_rule(
    "can_user_make_refusal_f680_outcome_letter",
    is_user_allocated & case_ready_for_outcome & all_releases_decided & release_has_refusal,
)
