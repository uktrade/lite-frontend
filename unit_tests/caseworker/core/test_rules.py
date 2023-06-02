import pytest
import rules

from django.http import HttpRequest

from caseworker.core import rules as caseworker_rules


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"  # /PS-IGNORE


def get_mock_request(user):
    request = HttpRequest()
    request.lite_user = user
    return request


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
def test_is_user_assigned(data, mock_gov_user, expected_result):
    assigned_users = {"assigned_users": data}
    assert caseworker_rules.is_user_assigned(get_mock_request(mock_gov_user["user"]), assigned_users) == expected_result


def test_is_user_case_officer_none():
    assert caseworker_rules.is_user_case_officer(get_mock_request(None), {"case_officer": None}) is False


@pytest.mark.parametrize(
    "data, expected_result",
    (
        ({"case_officer": {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"}}, False),  # /PS-IGNORE
        ({"case_officer": {"id": mock_gov_user_id}}, True),
        ({"case_officer": None}, False),
    ),
)
def test_is_user_case_officer(data, mock_gov_user, expected_result):
    assert caseworker_rules.is_user_case_officer(get_mock_request(mock_gov_user["user"]), data) == expected_result


@pytest.mark.parametrize(
    "data, expected_result",
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
            True,
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
            True,
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
            True,
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
            False,
        ),
    ),
)
def test_user_assignment_based_rules(data, mock_gov_user, expected_result):
    for rule_name in (
        "can_user_change_case",
        "can_user_move_case_forward",
        "can_user_review_and_countersign",
        "can_user_review_and_combine",
        "can_user_assess_products",
        "can_user_add_an_ejcu_query",
        "can_user_generate_document",
        "can_user_add_contact",
    ):
        assert rules.test_rule(rule_name, get_mock_request(mock_gov_user["user"]), data) == expected_result


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
def test_can_user_attach_document(data, mock_gov_user):
    assert rules.test_rule("can_user_attach_document", get_mock_request(mock_gov_user["user"]), data)
