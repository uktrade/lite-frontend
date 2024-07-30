import pytest
import requests
import rules

from django.http import HttpRequest

from core import client
from caseworker.advice.services import (
    GOODS_NOT_LISTED_ID,
    LICENSING_UNIT_TEAM,
    OGD_TEAMS,
)
from caseworker.core import rules as caseworker_rules
from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    FCDO_TEAM_ID,
    LICENSING_UNIT_TEAM_ID,
    TAU_TEAM_ID,
    LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID,
)
from core.constants import LicenceStatusEnum


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"  # /PS-IGNORE


@pytest.fixture
def get_mock_request(client):
    def request_factory(user):
        request = HttpRequest()
        request.lite_user = user
        request.session = client.session
        request.requests_session = requests.Session()
        return request

    return request_factory


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
def test_is_user_assigned(data, mock_gov_user, get_mock_request, expected_result):
    assigned_users = {"assigned_users": data}
    assert caseworker_rules.is_user_assigned(get_mock_request(mock_gov_user["user"]), assigned_users) is expected_result


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


def test_is_user_case_officer_none(get_mock_request):
    assert not caseworker_rules.is_user_case_officer(get_mock_request(None), {"case_officer": None})


@pytest.mark.parametrize(
    "data, expected_result",
    (
        ({"case_officer": {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"}}, False),  # /PS-IGNORE
        ({"case_officer": {"id": mock_gov_user_id}}, True),
        ({"case_officer": None}, False),
    ),
)
def test_is_user_case_officer(data, mock_gov_user, get_mock_request, expected_result):
    assert caseworker_rules.is_user_case_officer(get_mock_request(mock_gov_user["user"]), data) is expected_result


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
def test_user_assignment_based_rules(data, mock_gov_user, get_mock_request, expected_result):
    for rule_name in (
        "can_user_change_case",
        "can_user_move_case_forward",
        "can_user_review_and_countersign",
        "can_user_add_an_ejcu_query",
        "can_user_generate_document",
        "can_user_add_contact",
        "can_user_change_sub_status",
    ):
        assert rules.test_rule(rule_name, get_mock_request(mock_gov_user["user"]), data) is expected_result


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
def test_can_user_attach_document(data, mock_gov_user, get_mock_request):
    assert rules.test_rule("can_user_attach_document", get_mock_request(mock_gov_user["user"]), data)


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
    requests_mock, data_standard_case, mock_gov_user, get_mock_request, expected, sub_statuses
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
    request = get_mock_request(mock_gov_user["user"])
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
def test_can_user_search_products(mock_gov_user, get_mock_request, mock_gov_user_team, expected):
    user = mock_gov_user["user"]
    user["team"] = mock_gov_user_team

    request = get_mock_request(user)

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
def test_can_assigned_user_assess_products(mock_gov_user, get_mock_request, mock_gov_user_team, expected):
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

    request = get_mock_request(user)

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
def test_can_unassigned_user_assess_products(mock_gov_user, get_mock_request, mock_gov_user_team, expected):
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

    request = get_mock_request(user)

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
def test_can_user_review_and_combine_based_on_allocation(mock_gov_user, get_mock_request, case, expected_result):
    case["advice"] = [
        {
            "user": {"team": {"alias": OGD_TEAMS[0]}},
            "team": {"alias": OGD_TEAMS[0]},
        },
    ]

    user = mock_gov_user["user"]
    request = get_mock_request(user)

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
def test_can_user_review_and_combine_based_on_advice(mock_gov_user, get_mock_request, advice, flags, expected):
    case = {
        "advice": advice,
        "case_officer": {"id": mock_gov_user_id},
        "flags": flags,
    }

    user = mock_gov_user["user"]
    request = get_mock_request(user)

    assert rules.test_rule("can_user_review_and_combine", request, case) is expected


def test_can_user_rerun_routing_rules(get_mock_request):
    case = {}
    user = {}
    request = get_mock_request(user)
    assert not rules.test_rule("can_user_rerun_routing_rules", request, case)


@pytest.mark.parametrize(
    ("user_role_id", "licence_status", "expected"),
    (
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.ISSUED, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.ISSUED, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.REINSTATED, True),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.SUSPENDED, True),
        ("00c341d1-d83e-4a12-b103-c3fb575a5962", LicenceStatusEnum.ISSUED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.EXPIRED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.EXHAUSTED, False),
        (LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID, LicenceStatusEnum.CANCELLED, False),
    ),
)
def test_can_licence_status_be_changed(mock_gov_user, get_mock_request, user_role_id, licence_status, expected):
    licence = {
        "status": licence_status,
    }

    user = mock_gov_user["user"]
    user["role"]["id"] = user_role_id
    request = get_mock_request(user)
    user = request.lite_user

    assert rules.test_rule("can_licence_status_be_changed", user, licence) is expected
