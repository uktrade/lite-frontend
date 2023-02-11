import rules


@rules.predicate
def is_user_case_adviser(user, case):
    case_officer = case["case_officer"]
    if case_officer and user and user["id"] == case_officer.get("id"):
        return True
    return False


@rules.predicate
def is_user_assigned(user, case):
    if user and case["assigned_users"]:
        assigned_users_dict = case["assigned_users"].items()
        assigned_user = next(iter(assigned_users_dict))
        _, user_list = assigned_user
        for u in user_list:
            if u["id"] == user["id"]:
                return True
    return False


rules.add_rule("is_user_allowed_case_change", is_user_case_adviser | is_user_assigned)
