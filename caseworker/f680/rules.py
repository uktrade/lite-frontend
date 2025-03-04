import rules

from caseworker.core.rules import is_user_allocated, get_logged_in_caseworker
from caseworker.f680.recommendation.services import get_current_user_recommendation


@rules.predicate
def can_user_make_f680_recommendation(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    team = user["team"]["alias"]
    if get_current_user_recommendation(case.advice, user["id"], team):
        return False

    return True


rules.add_rule("can_user_make_f680_recommendation", is_user_allocated & can_user_make_f680_recommendation)
