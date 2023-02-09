import rules


@rules.predicate
def is_user_case_advisor(user_id, case):
    case_officer = case["case_officer"]
    if case_officer and user_id == case_officer.get("id"):
        return True
    return False


@rules.predicate
def is_user_assigned(user_id, case):
    if case["assigned_users"]:
        assigned_user = next(iter(case["assigned_users"].items()))
        _, user_list = assigned_user
        for u in user_list:
            if u["id"] == user_id:
                return True
    return False


rules.add_rule("is_user_case_advisor_or_assigned_user", is_user_case_advisor | is_user_assigned)
