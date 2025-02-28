import rules

from caseworker.core.rules import is_user_allocated, get_logged_in_caseworker
from caseworker.f680.recommendation.services import get_current_user_recommendation


@rules.predicate
def has_user_made_recommendation(case, user):
    team = user["team"]["alias"]
    return get_current_user_recommendation(case.advice, user["id"], team)


@rules.predicate
def can_user_make_f680_recommendation(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    if has_user_made_recommendation(case, user):
        return False

    return True


rules.add_rule("can_user_make_f680_recommendation", is_user_allocated & can_user_make_f680_recommendation)
