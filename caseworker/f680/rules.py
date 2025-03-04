import rules

from caseworker.core.rules import is_user_allocated, get_logged_in_caseworker
from caseworker.f680.recommendation.services import get_current_user_recommendation, filter_recommendation_by_team


@rules.predicate
def can_user_make_f680_recommendation(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    team = user["team"]["alias"]
    if get_current_user_recommendation(case.advice, user["id"], team):
        return False

    return case["data"]["status"]["key"] == "ogd_advice"


@rules.predicate
def case_ready_for_outcome(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    return case["data"]["status"]["key"] == "under_final_review"


@rules.predicate
def f680_case_ready_for_move(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False
    case_status = case["data"]["status"]["key"]

    if case_status == "submitted":
        return True

    if case_status == "ogd_advice":
        team = user["team"]["alias"]
        team_recommendations_exist = bool(filter_recommendation_by_team(case.advice, team))
        if team_recommendations_exist:
            return True

        # TODO: Remove this once we get stop the case going to MOD-ECJU Review and combine
        if team == "MOD_ECJU":
            return True

    return False


rules.add_rule("can_user_make_f680_recommendation", is_user_allocated & can_user_make_f680_recommendation)
rules.add_rule("can_user_generate_f680_outcome_document", is_user_allocated & case_ready_for_outcome)
rules.add_rule("can_user_move_f680_case_forward", is_user_allocated & f680_case_ready_for_move)
