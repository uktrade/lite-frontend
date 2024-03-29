import rules

from caseworker.core.constants import ADMIN_TEAM_ID, TAU_TEAM_ID
from caseworker.cases.services import get_case_sub_statuses


@rules.predicate
def has_available_sub_statuses(request, case):
    return bool(get_case_sub_statuses(request, case["id"]))


@rules.predicate
def is_user_case_officer(request, case):
    try:
        user = request.lite_user
    except AttributeError:
        return False
    case_officer = case["case_officer"]
    return case_officer is not None and user and user["id"] == case_officer.get("id")


@rules.predicate
def is_user_assigned(request, case):
    try:
        user = request.lite_user
    except AttributeError:
        return False
    if user and case["assigned_users"]:
        # Loop through all queues to check if user is assigned
        for _, assigned_users in case["assigned_users"].items():
            if any(u["id"] == user["id"] for u in assigned_users):
                return True
    return False


is_user_allocated = is_user_case_officer | is_user_assigned  # noqa


@rules.predicate
def is_user_in_admin_team(request):
    user = getattr(request, "lite_user", None)
    return user and user.get("team", {}).get("id") == ADMIN_TEAM_ID


@rules.predicate
def is_user_in_tau_team(request):
    user = getattr(request, "lite_user", None)
    return user and user.get("team", {}).get("id") == TAU_TEAM_ID


rules.add_rule("can_user_change_case", is_user_allocated)
rules.add_rule("can_user_move_case_forward", is_user_allocated)
rules.add_rule("can_user_review_and_countersign", is_user_allocated)
rules.add_rule("can_user_review_and_combine", is_user_allocated)
rules.add_rule("can_user_assess_products", is_user_allocated & (is_user_in_tau_team | is_user_in_admin_team))  # noqa
rules.add_rule("can_user_add_an_ejcu_query", is_user_allocated)
rules.add_rule("can_user_attach_document", rules.always_allow)
rules.add_rule("can_user_generate_document", is_user_allocated)
rules.add_rule("can_user_add_contact", is_user_allocated)
rules.add_rule("can_user_change_sub_status", is_user_allocated & has_available_sub_statuses)
rules.add_rule("can_user_search_products", is_user_in_admin_team | is_user_in_tau_team)  # noqa
