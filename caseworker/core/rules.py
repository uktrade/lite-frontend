import rules

from caseworker.advice.services import (
    filter_advice_by_teams,
    GOODS_NOT_LISTED_ID,
    OGD_TEAMS,
)
from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    TAU_TEAM_ID,
    LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID,
    SUPER_USER_ROLE_ID,
)
from caseworker.cases.services import get_case_sub_statuses
from caseworker.flags.helpers import has_flag
from core.constants import LicenceStatusEnum


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


@rules.predicate
def case_has_ogd_advice(request, case):
    if not case["advice"]:
        return False

    if not filter_advice_by_teams(case["advice"], OGD_TEAMS):
        return False

    return True


@rules.predicate
def case_is_nlr(request, case):
    return has_flag(case, GOODS_NOT_LISTED_ID)


@rules.predicate
def is_user_licencing_unit_senior_manager(user):
    user_role_id = user["role"]["id"]
    return user_role_id in [LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, SUPER_USER_ROLE_ID]


@rules.predicate
def is_license_in_editable_state(user, licence):
    return licence["status"] in [
        LicenceStatusEnum.ISSUED,
        LicenceStatusEnum.REINSTATED,
        LicenceStatusEnum.SUSPENDED,
    ]


rules.add_rule("can_user_change_case", is_user_allocated)
rules.add_rule("can_user_move_case_forward", is_user_allocated)
rules.add_rule("can_user_review_and_countersign", is_user_allocated)
rules.add_rule("can_user_review_and_combine", is_user_allocated & (case_has_ogd_advice | case_is_nlr))  # noqa
rules.add_rule("can_user_assess_products", is_user_allocated & (is_user_in_tau_team | is_user_in_admin_team))  # noqa
rules.add_rule("can_user_add_an_ejcu_query", is_user_allocated)
rules.add_rule("can_user_attach_document", rules.always_allow)
rules.add_rule("can_user_generate_document", is_user_allocated)
rules.add_rule("can_user_add_contact", is_user_allocated)
rules.add_rule("can_user_change_sub_status", is_user_allocated & has_available_sub_statuses)
rules.add_rule("can_user_search_products", is_user_in_admin_team | is_user_in_tau_team)  # noqa
rules.add_rule("can_user_rerun_routing_rules", rules.always_deny)
rules.add_rule("can_licence_status_be_changed", is_user_licencing_unit_senior_manager & is_license_in_editable_state)
