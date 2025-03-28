import rules

from core.constants import CaseStatusEnum

from caseworker.core.rules import is_user_allocated, get_logged_in_caseworker
from caseworker.f680.recommendation.services import (
    recommendations_by_current_user,
    filter_recommendation_by_team,
    get_case_recommendations,
)


RECOMMENDATION_STATUSES = [CaseStatusEnum.OGD_ADVICE]
OUTCOME_STATUSES = [CaseStatusEnum.UNDER_FINAL_REVIEW]
INFORMATIONAL_STATUSES = [CaseStatusEnum.SUBMITTED]


@rules.predicate
def is_user_allowed_to_make_f680_recommendation(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    return case["data"]["status"]["key"] in RECOMMENDATION_STATUSES + OUTCOME_STATUSES


@rules.predicate
def can_user_make_f680_recommendation(request, case):
    # TODO: change this snippet in to a decorator? We seem to use it for every rule
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    if recommendations_by_current_user(request, case, user):
        return False

    return case["data"]["status"]["key"] in RECOMMENDATION_STATUSES


@rules.predicate
def can_user_clear_f680_recommendation(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    return bool(recommendations_by_current_user(request, case, user))


@rules.predicate
def f680_case_ready_for_move(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False
    case_status = case["data"]["status"]["key"]

    if case_status in INFORMATIONAL_STATUSES:
        return True

    if case_status in RECOMMENDATION_STATUSES:
        case_recommendations = get_case_recommendations(request, case)

        team = user["team"]
        team_recommendations_exist = bool(filter_recommendation_by_team(case_recommendations, team["id"]))
        if team_recommendations_exist:
            return True

        # TODO: Remove this once we get stop the case going to MOD-ECJU Review and combine
        if team["alias"] == "MOD_ECJU":
            return True

    return False


@rules.predicate
def case_ready_for_outcome(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    return case["data"]["status"]["key"] in OUTCOME_STATUSES


rules.add_rule(
    "is_user_allowed_to_make_f680_recommendation", is_user_allocated & is_user_allowed_to_make_f680_recommendation
)
rules.add_rule("can_user_make_f680_recommendation", is_user_allocated & can_user_make_f680_recommendation)
rules.add_rule("can_user_clear_f680_recommendation", is_user_allocated & can_user_clear_f680_recommendation)
rules.add_rule("can_user_make_f680_outcome", is_user_allocated & case_ready_for_outcome)
rules.add_rule("can_user_move_f680_case_forward", is_user_allocated & f680_case_ready_for_move)
