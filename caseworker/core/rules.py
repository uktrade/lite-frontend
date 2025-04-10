import rules

from django.conf import settings

from caseworker.advice.constants import AdviceLevel
from caseworker.advice.services import (
    GOODS_NOT_LISTED_ID,
    OGD_TEAMS,
    LICENSING_UNIT_TEAM,
    filter_advice_by_teams,
    filter_advice_by_level,
    get_final_advisers,
    get_countersigners_decision_advice,
)
from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    SUPER_USER_ROLE_ID,
    TAU_TEAM_ID,
    LICENSING_UNIT_TEAM_ID,
    LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID,
    Permission,
)
from caseworker.cases.services import get_case_sub_statuses
from caseworker.core.services import get_caseworker_operable_case_statuses
from caseworker.flags.helpers import has_flag
from core.constants import CaseStatusEnum, LicenceStatusEnum


def get_logged_in_caseworker(request):
    try:
        user = request.lite_user
    except AttributeError:
        return False

    return user


@rules.predicate
def has_available_sub_statuses(request, case):
    return bool(get_case_sub_statuses(request, case["id"]))


@rules.predicate
def is_user_case_officer(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
        return False

    case_officer = case["case_officer"]
    return case_officer is not None and user and user["id"] == case_officer.get("id")


@rules.predicate
def is_user_assigned(request, case):
    user = get_logged_in_caseworker(request)
    if not user:
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
def is_user_in_lu_team(request):
    user = get_logged_in_caseworker(request)
    if not user:
        return False
    return user and user.get("team", {}).get("id") == LICENSING_UNIT_TEAM_ID


@rules.predicate
def case_has_ogd_advice(request, case):
    if not case["advice"]:
        return False

    if not filter_advice_by_teams(case["advice"], OGD_TEAMS):
        return False

    return True


@rules.predicate
def case_has_final_advice(request, case):
    if not case["advice"]:
        return False

    if not case_has_ogd_advice(request, case):
        return False

    final_advice = filter_advice_by_level(case["advice"], [AdviceLevel.FINAL])
    final_advice_from_lu = [advice for advice in final_advice if advice["team"]["alias"] == LICENSING_UNIT_TEAM]
    return len(final_advice_from_lu) > 0


@rules.predicate
def is_case_nlr(request, case):
    return has_flag(case, GOODS_NOT_LISTED_ID)


@rules.predicate
def is_user_licencing_unit_senior_manager(request):
    user = getattr(request, "lite_user", None)

    user_role_id = user["role"]["id"]
    return user_role_id == LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID


@rules.predicate
def is_case_finalised_and_licence_editable(request, licence):
    is_case_finalised = licence.get("case_status") == CaseStatusEnum.FINALISED
    is_licence_editable = licence.get("status").lower() in [
        LicenceStatusEnum.ISSUED,
        LicenceStatusEnum.REINSTATED,
        LicenceStatusEnum.SUSPENDED,
    ]

    return is_case_finalised and is_licence_editable


@rules.predicate
def is_case_caseworker_operable(request, case):
    caseworker = get_logged_in_caseworker(request)
    if not caseworker:
        return False

    return case.status in get_caseworker_operable_case_statuses(request)


@rules.predicate
def user_is_not_final_adviser(request, case):

    caseworker = get_logged_in_caseworker(request)
    if not caseworker:
        return False

    case_officer = case["case_officer"]
    case_officer = {case_officer.get("id", {})} if case_officer else set()
    final_advisers = get_final_advisers(case)
    all_advisers = case_officer | final_advisers

    return caseworker["id"] not in all_advisers


@rules.predicate
def user_not_yet_countersigned(request, case):

    caseworker = get_logged_in_caseworker(request)
    if not caseworker:
        return False

    countersigners = get_countersigners_decision_advice(case, caseworker)

    return caseworker["id"] not in countersigners


@rules.predicate
def is_user_manage_organisations_role(request, organisation):
    user = getattr(request, "lite_user", None)
    return user and Permission.MANAGE_ORGANISATIONS.value in user["role"]["permissions"]


@rules.predicate
def is_organisation_active(request, organisation):
    return organisation["status"]["key"] == "active"


@rules.predicate
def is_super_user(request):
    user = get_logged_in_caseworker(request)
    return user.get("role", {}).get("id") == SUPER_USER_ROLE_ID


@rules.predicate
def check_user_is_not_logged_in_caseworker(request, user):
    if not user:
        return True
    caseworker = get_logged_in_caseworker(request)
    caseworker_user_id = caseworker["id"]
    is_actioned_user_not_current_user = user.get("user", {}).get("id") != caseworker_user_id
    return is_actioned_user_not_current_user


@rules.predicate
def is_f680_feature_flag_enabled(request):
    return settings.FEATURE_FLAG_ALLOW_F680


rules.add_rule("can_user_allocate_case", is_case_caseworker_operable)
rules.add_rule("can_user_change_case", is_user_allocated)
rules.add_rule("can_user_move_case_forward", is_user_allocated)
rules.add_rule("can_user_review_and_countersign", is_user_allocated)
rules.add_rule(
    "can_user_be_allowed_to_lu_countersign",
    is_user_allocated
    & is_user_in_lu_team
    & case_has_final_advice
    & user_is_not_final_adviser
    & user_not_yet_countersigned,
)
rules.add_rule("can_user_review_and_combine", is_user_allocated & (case_has_ogd_advice | is_case_nlr))  # noqa
rules.add_rule("can_user_assess_products", is_user_allocated & (is_user_in_tau_team | is_user_in_admin_team))  # noqa
rules.add_rule("can_user_add_an_ecju_query", is_user_allocated)
rules.add_rule("can_user_attach_document", rules.always_allow)
rules.add_rule("can_user_generate_document", is_user_allocated)
rules.add_rule("can_user_add_contact", is_user_allocated)
rules.add_rule("can_user_change_sub_status", is_user_allocated & has_available_sub_statuses)
rules.add_rule("can_user_search_products", is_user_in_admin_team | is_user_in_tau_team)  # noqa
rules.add_rule("can_user_rerun_routing_rules", rules.always_deny)
rules.add_rule(
    "can_licence_status_be_changed", is_user_licencing_unit_senior_manager & is_case_finalised_and_licence_editable
)
rules.add_rule("can_user_manage_organisation", is_user_manage_organisations_role & is_organisation_active)
rules.add_rule("can_caseworker_deactivate", (is_super_user) & check_user_is_not_logged_in_caseworker)  # noqa
rules.add_rule("can_caseworker_edit_user", (is_super_user))  # noqa
rules.add_rule("can_caseworker_add_user", (is_super_user))  # noqa
rules.add_rule("can_user_modify_f680", is_f680_feature_flag_enabled)
