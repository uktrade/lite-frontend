import pytest
import rules
import uuid


from core import client
from caseworker.advice.constants import AdviceLevel
from caseworker.advice.services import (
    GOODS_NOT_LISTED_ID,
    LICENSING_UNIT_TEAM,
    OGD_TEAMS,
    FIRST_COUNTERSIGN,
    SECOND_COUNTERSIGN,
)
from caseworker.core import rules as caseworker_rules
from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    FCDO_TEAM_ID,
    LICENSING_UNIT_TEAM_ID,
    SUPER_USER_ROLE_ID,
    TAU_TEAM_ID,
    LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID,
    Permission,
)
from core.constants import CaseStatusEnum, LicenceStatusEnum
from caseworker.cases.objects import Case


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"  # /PS-IGNORE


@pytest.mark.parametrize(
    "data, expected_result",
    (
        (
            {
                "fake queue": [
                    {"id": mock_gov_user_id},
                ],
                "fake queue 2": [
                    {"id": "12345zyz"},
                ],
            },
            True,
        ),
        (
            {
                "fake queue": [
                    {"id": "12345zyz"},
                ],
                "fake queue 2": [
                    {"id": mock_gov_user_id},
                ],
            },
            True,
        ),
        (
            {
                "fake queue": [
                    {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"},  # /PS-IGNORE
                ]
            },
            False,
        ),
        ({"fake queue": []}, False),
    ),
)
def test_is_user_assigned(data, mock_gov_user, get_mock_request_user, expected_result):
    assigned_users = {"assigned_users": data}
    assert (
        caseworker_rules.is_user_assigned(get_mock_request_user(mock_gov_user["user"]), assigned_users)
        is expected_result
    )


def test_is_user_assigned_request_missing_attribute():
    assigned_users = {
        "assigned_users": {
            "fake queue": [
                {"id": mock_gov_user_id},
            ],
            "fake queue 2": [
                {"id": "12345zyz"},
            ],
        },
    }
    assert not caseworker_rules.is_user_assigned(None, assigned_users)


def test_is_user_case_officer_none(get_mock_request_user):
    assert not caseworker_rules.is_user_case_officer(get_mock_request_user(None), {"case_officer": None})


@pytest.mark.parametrize(
    "data, expected_result",
    (
        ({"case_officer": {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"}}, False),  # /PS-IGNORE
        ({"case_officer": {"id": mock_gov_user_id}}, True),
        ({"case_officer": None}, False),
    ),
)
def test_is_user_case_officer(data, mock_gov_user, get_mock_request_user, expected_result):
    assert caseworker_rules.is_user_case_officer(get_mock_request_user(mock_gov_user["user"]), data) is expected_result


def test_is_user_case_officer_request_missing_attribute():
    assert caseworker_rules.is_user_case_officer(None, {"case_officer": {"id": mock_gov_user_id}}) is False


@pytest.mark.parametrize(
    "data, expected_result",
    (
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
            False,
        ),
    ),
)
def test_user_assignment_based_rules(data, mock_gov_user, get_mock_request_user, expected_result):
    for rule_name in (
        "can_user_change_case",
        "can_user_move_case_forward",
        "can_user_review_and_countersign",
        "can_user_add_an_ejcu_query",
        "can_user_generate_document",
        "can_user_add_contact",
        "can_user_change_sub_status",
    ):
        assert rules.test_rule(rule_name, get_mock_request_user(mock_gov_user["user"]), data) is expected_result


@pytest.mark.parametrize(
    "data",
    (
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
        ),
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
        ),
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
        ),
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
        ),
    ),
)
def test_can_user_attach_document(data, mock_gov_user, get_mock_request_user):
    assert rules.test_rule("can_user_attach_document", get_mock_request_user(mock_gov_user["user"]), data)


@pytest.mark.parametrize(
    "sub_statuses, expected",
    (
        ([], False),
        (
            [
                {
                    "id": "status-1",
                    "name": "Status 1",
                }
            ],
            True,
        ),
    ),
)
def test_can_use_change_sub_status(
    requests_mock, data_standard_case, mock_gov_user, get_mock_request_user, expected, sub_statuses
):
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(
        client._build_absolute_uri(f"/applications/{case_id}/sub-statuses/"),
        json=sub_statuses,
    )
    assigned_case = {
        "id": case_id,
        "assigned_users": {
            "fake queue": [
                {"id": mock_gov_user_id},
            ]
        },
        "case_officer": {"id": mock_gov_user_id},
    }
    request = get_mock_request_user(mock_gov_user["user"])
    assert rules.test_rule("can_user_change_sub_status", request, assigned_case) is expected


@pytest.mark.parametrize(
    ("mock_gov_user_team", "expected"),
    (
        ({"id": ADMIN_TEAM_ID, "name": "Admin", "alias": None}, True),
        ({"id": TAU_TEAM_ID, "name": "TAU", "alias": "TAU"}, True),
        ({"id": FCDO_TEAM_ID, "name": "FCDO", "alias": "FCO"}, False),
        ({"id": LICENSING_UNIT_TEAM_ID, "name": "Licensing Unit", "alias": "LICENSING_UNIT"}, False),
    ),
)
def test_can_user_search_products(mock_gov_user, get_mock_request_user, mock_gov_user_team, expected):
    user = mock_gov_user["user"]
    user["team"] = mock_gov_user_team

    request = get_mock_request_user(user)

    assert rules.test_rule("can_user_search_products", request) is expected


@pytest.mark.parametrize(
    ("mock_gov_user_team", "expected"),
    (
        ({"id": ADMIN_TEAM_ID, "name": "Admin", "alias": None}, True),
        ({"id": TAU_TEAM_ID, "name": "TAU", "alias": "TAU"}, True),
        ({"id": FCDO_TEAM_ID, "name": "FCDO", "alias": "FCO"}, False),
        ({"id": LICENSING_UNIT_TEAM_ID, "name": "Licensing Unit", "alias": "LICENSING_UNIT"}, False),
    ),
)
def test_can_assigned_user_assess_products(mock_gov_user, get_mock_request_user, mock_gov_user_team, expected):
    user = mock_gov_user["user"]
    case = {
        "assigned_users": {
            "fake queue": [
                {"id": user["id"]},
            ]
        },
        "case_officer": {"id": user["id"]},
    }

    user["team"] = mock_gov_user_team

    request = get_mock_request_user(user)

    assert rules.test_rule("can_user_assess_products", request, case) is expected


@pytest.mark.parametrize(
    ("mock_gov_user_team", "expected"),
    (
        ({"id": ADMIN_TEAM_ID, "name": "Admin", "alias": None}, False),
        ({"id": TAU_TEAM_ID, "name": "TAU", "alias": "TAU"}, False),
        ({"id": FCDO_TEAM_ID, "name": "FCDO", "alias": "FCO"}, False),
        ({"id": LICENSING_UNIT_TEAM_ID, "name": "Licensing Unit", "alias": "LICENSING_UNIT"}, False),
    ),
)
def test_can_unassigned_user_assess_products(mock_gov_user, get_mock_request_user, mock_gov_user_team, expected):
    case = {
        "assigned_users": {
            "fake queue": [
                {"id": "some-other-user-id"},
            ]
        },
        "case_officer": {"id": "some-other-user-id"},
    }

    user = mock_gov_user["user"]
    user["team"] = mock_gov_user_team

    request = get_mock_request_user(user)

    assert rules.test_rule("can_user_assess_products", request, case) is expected


@pytest.mark.parametrize(
    "case, expected_result",
    (
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": mock_gov_user_id},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": mock_gov_user_id},
            },
            True,
        ),
        (
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",  # /PS-IGNORE
                "assigned_users": {
                    "fake queue": [
                        {"id": "fake_id"},
                    ]
                },
                "case_officer": {"id": "fake_id"},
            },
            False,
        ),
    ),
)
def test_can_user_review_and_combine_based_on_allocation(mock_gov_user, get_mock_request_user, case, expected_result):
    case["advice"] = [
        {
            "user": {"team": {"alias": OGD_TEAMS[0]}},
            "team": {"alias": OGD_TEAMS[0]},
        },
    ]

    user = mock_gov_user["user"]
    request = get_mock_request_user(user)

    assert rules.test_rule("can_user_review_and_combine", request, case) is expected_result


@pytest.mark.parametrize(
    ("advice", "flags", "expected"),
    (
        (
            [],
            [],
            False,
        ),
        (
            [],
            [{"id": GOODS_NOT_LISTED_ID}],
            True,
        ),
        (
            [
                {"user": {"team": {"alias": LICENSING_UNIT_TEAM}}, "team": {"alias": LICENSING_UNIT_TEAM}},
            ],
            [],
            False,
        ),
        *[([{"user": {"team": {"alias": alias}}, "team": {"alias": alias}}], [], True) for alias in OGD_TEAMS],
    ),
)
def test_can_user_review_and_combine_based_on_advice(mock_gov_user, get_mock_request_user, advice, flags, expected):
    case = {
        "advice": advice,
        "case_officer": {"id": mock_gov_user_id},
        "flags": flags,
    }

    user = mock_gov_user["user"]
    request = get_mock_request_user(user)

    assert rules.test_rule("can_user_review_and_combine", request, case) is expected


def test_can_user_rerun_routing_rules(get_mock_request_user):
    case = {}
    user = {}
    request = get_mock_request_user(user)
    assert not rules.test_rule("can_user_rerun_routing_rules", request, case)


@pytest.mark.parametrize(
    ("user_role_id", "licence_status", "case_status", "expected"),
    (
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.ISSUED, CaseStatusEnum.FINALISED, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.REINSTATED, CaseStatusEnum.FINALISED, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.SUSPENDED, CaseStatusEnum.FINALISED, True),
        (str(uuid.uuid4()), LicenceStatusEnum.ISSUED, CaseStatusEnum.FINALISED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.EXPIRED, CaseStatusEnum.FINALISED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.EXHAUSTED, CaseStatusEnum.FINALISED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.CANCELLED, CaseStatusEnum.FINALISED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.ISSUED, CaseStatusEnum.SUSPENDED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.ISSUED, CaseStatusEnum.WITHDRAWN, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.SUSPENDED, CaseStatusEnum.SUSPENDED, False),
    ),
)
def test_can_licence_status_be_changed(
    mock_gov_user, get_mock_request_user, user_role_id, licence_status, case_status, expected, data_standard_case
):
    case = Case(data_standard_case["case"])

    case.licences = [
        {
            "id": str(uuid.uuid4()),
            "reference_code": "GBSIEL/2000/0000001/P",
            "status": licence_status,
            "case_status": case_status,
            "goods": [],
        },
    ]

    licence = case.licences[0]

    user = mock_gov_user["user"]
    user["role"]["id"] = user_role_id
    request = get_mock_request_user(user)

    assert rules.test_rule("can_licence_status_be_changed", request, licence) is expected


@pytest.mark.parametrize(
    "gov_user, expected_result",
    (
        ("invalid_user", False),
        ("LU_case_officer", True),
        ("LU_licensing_manager", True),
        ("LU_senior_licensing_manager", True),
        ("FCDO_team_user", False),
    ),
)
def test_is_user_in_lu_team(gov_user, get_mock_request_user, expected_result, request):
    user = request.getfixturevalue(gov_user)
    assert caseworker_rules.is_user_in_lu_team(get_mock_request_user(user)) == expected_result


@pytest.mark.parametrize(
    "advice_data, expected_result",
    (
        ([], False),
        ([{"type": "approve", "level": AdviceLevel.USER, "team": {"name": "FCDO", "alias": "FCO"}}], False),
        ([{"type": "approve", "level": AdviceLevel.USER, "team": {"name": "MOD_DI", "alias": "MOD_DI"}}], False),
        ([{"type": "approve", "level": AdviceLevel.USER, "team": {"name": "MOD_DSR", "alias": "MOD_DSR"}}], False),
        (
            [
                {
                    "type": "approve",
                    "level": AdviceLevel.USER,
                    "team": {"name": "LICENSING_UNIT", "alias": "LICENSING_UNIT"},
                }
            ],
            False,
        ),
        (
            [
                {"type": "approve", "level": AdviceLevel.USER, "team": {"name": "FCDO", "alias": "FCO"}},
                {
                    "type": "approve",
                    "level": AdviceLevel.TEAM,
                    "team": {"name": "LICENSING_UNIT", "alias": "LICENSING_UNIT"},
                },
            ],
            False,
        ),
        (
            [
                {"type": "approve", "level": AdviceLevel.USER, "team": {"name": "FCDO", "alias": "FCO"}},
                {
                    "type": "approve",
                    "level": AdviceLevel.FINAL,
                    "team": {"name": "LICENSING_UNIT", "alias": "LICENSING_UNIT"},
                },
            ],
            True,
        ),
    ),
)
def test_case_has_final_advice(advice_data, mock_gov_user, get_mock_request_user, expected_result):
    request = get_mock_request_user(mock_gov_user["user"])
    case = {"advice": advice_data}
    assert caseworker_rules.case_has_final_advice(request, case) is expected_result


@pytest.fixture
def invalid_user():
    return {}


@pytest.mark.parametrize(
    "gov_user, expected_result",
    (
        ("invalid_user", False),
        ("LU_case_officer", False),
        ("LU_licensing_manager", True),
        ("LU_senior_licensing_manager", True),
    ),
)
def test_user_is_not_final_adviser(gov_user, expected_result, request, get_mock_request_user, LU_case_officer):
    case = {
        "case_officer": LU_case_officer,
        "advice": [
            {
                "level": AdviceLevel.FINAL,
                "user": LU_case_officer,
            },
        ],
    }
    user = request.getfixturevalue(gov_user)
    assert caseworker_rules.user_is_not_final_adviser(get_mock_request_user(user), case) == expected_result


@pytest.mark.parametrize(
    "gov_user, countersigners, expected_result",
    (
        ("invalid_user", [], False),
        ("LU_licensing_manager", [], True),
        ("LU_licensing_manager", [{"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"}], False),
        ("LU_senior_licensing_manager", [{"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"}], True),
        (
            "LU_senior_licensing_manager",
            [
                {"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"},
                {"order": SECOND_COUNTERSIGN, "user": "LU_senior_licensing_manager"},
            ],
            False,
        ),
    ),
)
def test_user_not_yet_countersigned(
    gov_user, countersigners, expected_result, request, get_mock_request_user, LU_case_officer
):
    countersign_advice = [
        {
            "valid": True,
            "order": item["order"],
            "countersigned_user": request.getfixturevalue(item["user"]),
        }
        for item in countersigners
    ]
    case = Case(
        {
            "case_officer": LU_case_officer,
            "advice": [
                {
                    "level": AdviceLevel.FINAL,
                    "user": LU_case_officer,
                },
            ],
            "countersign_advice": countersign_advice,
        }
    )
    user = request.getfixturevalue(gov_user)
    assert caseworker_rules.user_not_yet_countersigned(get_mock_request_user(user), case) == expected_result


@pytest.mark.parametrize(
    "gov_user, countersigners, expected_result",
    (
        ("invalid_user", [], False),
        ("LU_case_officer", [], False),
        ("LU_licensing_manager", [], True),
        ("LU_licensing_manager", [{"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"}], False),
        ("LU_senior_licensing_manager", [{"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"}], True),
        (
            "LU_senior_licensing_manager",
            [
                {"order": FIRST_COUNTERSIGN, "user": "LU_licensing_manager"},
                {"order": SECOND_COUNTERSIGN, "user": "LU_senior_licensing_manager"},
            ],
            False,
        ),
    ),
)
def test_can_user_be_allowed_to_lu_countersign(
    gov_user, countersigners, expected_result, request, get_mock_request_user, FCDO_team_user, LU_case_officer
):
    countersign_advice = [
        {
            "valid": True,
            "order": item["order"],
            "countersigned_user": request.getfixturevalue(item["user"]),
        }
        for item in countersigners
    ]

    user = request.getfixturevalue(gov_user)
    case = Case(
        {
            "case_officer": LU_case_officer,
            "assigned_users": {"fake queue": [user]},
            "advice": [
                {
                    "level": AdviceLevel.USER,
                    "user": FCDO_team_user,
                    "team": FCDO_team_user["team"],
                },
                {
                    "level": AdviceLevel.FINAL,
                    "user": LU_case_officer,
                    "team": LU_case_officer["team"],
                },
            ],
            "countersign_advice": countersign_advice,
        }
    )

    assert (
        rules.test_rule("can_user_be_allowed_to_lu_countersign", get_mock_request_user(user), case) is expected_result
    )


@pytest.mark.parametrize(
    ("user_permission", "organisation_status", "expected"),
    (
        ([Permission.MANAGE_ORGANISATIONS.value], "active", True),
        ([Permission.MANAGE_ORGANISATIONS.value, Permission.ADMINISTER_ROLES.value], "active", True),
        ([Permission.ADMINISTER_ROLES.value], "active", False),
        ([], "active", False),
        ([Permission.MANAGE_ORGANISATIONS.value], "in-review", False),
        ([Permission.ADMINISTER_ROLES.value], "in-review", False),
        ([], "in-review", False),
    ),
)
def test_can_user_manage_organisation(
    mock_gov_user, get_mock_request_user, user_permission, organisation_status, expected, data_organisation
):

    user = mock_gov_user["user"]
    user["role"]["permissions"] = user_permission
    request = get_mock_request_user(user)
    data_organisation["status"]["key"] = organisation_status
    assert rules.test_rule("can_user_manage_organisation", request, data_organisation) is expected


@pytest.mark.parametrize(
    ("user_role", "user_team", "expected"),
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
        (SUPER_USER_ROLE_ID, TAU_TEAM_ID, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, ADMIN_TEAM_ID, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, TAU_TEAM_ID, False),
        (None, None, False),
    ),
)
def test_can_caseworker_add_edit_role(mock_gov_user, get_mock_request_user, user_team, user_role, expected):
    user = mock_gov_user["user"]
    user["role"]["id"] = user_role
    user["team"]["id"] = user_team
    request = get_mock_request_user(user)
    assert rules.test_rule("can_caseworker_edit_user", request) is expected
    assert rules.test_rule("can_caseworker_add_user", request) is expected


@pytest.mark.parametrize(
    ("user_role", "user_team", "user_data", "expected"),
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, {"user": {"id": "123"}}, True),
        (SUPER_USER_ROLE_ID, TAU_TEAM_ID, {"user": {"id": "123"}}, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, ADMIN_TEAM_ID, {"user": {"id": "123"}}, False),
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, {"user": {"id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0"}}, False),
        (SUPER_USER_ROLE_ID, TAU_TEAM_ID, {"user": {"id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0"}}, False),
        (
            SUPER_USER_ROLE_ID,
            ADMIN_TEAM_ID,
            {"user": {"id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0"}},
            False,
        ),
        (None, None, None, False),
    ),
)
def test_can_caseworker_deactivate(mock_gov_user, get_mock_request_user, user_team, user_role, user_data, expected):

    user = mock_gov_user["user"]
    user["role"]["id"] = user_role
    user["team"]["id"] = user_team
    request = get_mock_request_user(user)
    assert rules.test_rule("can_caseworker_deactivate", request, user_data) is expected
