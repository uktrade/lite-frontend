import rules

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

rules.add_rule("can_user_change_case", is_user_allocated)
rules.add_rule("can_user_move_case_forward", is_user_allocated)
rules.add_rule("can_user_review_and_countersign", is_user_allocated)
rules.add_rule("can_user_review_and_combine", is_user_allocated)
rules.add_rule("can_user_assess_products", is_user_allocated)
rules.add_rule("can_user_add_an_ejcu_query", is_user_allocated)
rules.add_rule("can_user_attach_document", rules.always_allow)
rules.add_rule("can_user_generate_document", is_user_allocated)
rules.add_rule("can_user_add_contact", is_user_allocated)
rules.add_rule("can_user_change_sub_status", is_user_allocated & has_available_sub_statuses)
