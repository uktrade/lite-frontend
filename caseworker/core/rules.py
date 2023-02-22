import rules


@rules.predicate
def is_user_case_adviser(user, case):
    case_officer = case["case_officer"]
    return case_officer is not None and user and user["id"] == case_officer.get("id")


@rules.predicate
def is_user_assigned(user, case):
    if user and case["assigned_users"]:
        assigned_users_dict = case["assigned_users"].items()
        assigned_user = next(iter(assigned_users_dict))
        _, user_list = assigned_user
        return any(u["id"] == user["id"] for u in user_list)
    return False


rules.add_rule("can_user_change_case", is_user_case_adviser | is_user_assigned)
rules.add_rule("can_user_move_case_forward", is_user_case_adviser | is_user_assigned)
