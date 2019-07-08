def get_assigned_users_from_cases(case_ids: list, case_assignments: list) -> list:
    """
    Return a list of users if the case they're in belongs to the list of cases given in case_ids
    """
    assigned_users = []

    for assignment in (x for x in case_assignments if x['case'] in case_ids):
        assigned_users.extend(assignment['users'])

    return assigned_users


def add_assigned_users_to_cases(cases: list, case_assignments: list) -> list:
    """
    If a user is assigned to a case via queue case assignment, add them as a key on the case
    """
    for case in cases:
        for case_assignment in case_assignments:
            if case_assignment['case'] == case['id']:
                case['assignments'] = case_assignment['users']

    return cases
