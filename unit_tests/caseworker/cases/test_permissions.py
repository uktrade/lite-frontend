import pytest
import rules

from caseworker.cases.views import permissions

user_id = "a787705e-9b5f-449d-bde0-ea4d29aeab83"


@pytest.mark.parametrize(
    "data, expected_result",
    (
        ({"case_officer": {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"}}, False),  # /PS-IGNORE
        ({"case_officer": {"id": "a787705e-9b5f-449d-bde0-ea4d29aeab83"}}, True),  # /PS-IGNORE
        ({"case_officer": None}, False),
    ),
)
def test_is_user_case_officer(data, expected_result):
    user_id = "a787705e-9b5f-449d-bde0-ea4d29aeab83"
    assert permissions.is_user_case_advisor(user_id, data) == expected_result


@pytest.mark.parametrize(
    "data, expected_result",
    (
        (
            {
                "fake queue": [
                    {"id": "a787705e-9b5f-449d-bde0-ea4d29aeab83"},  # /PS-IGNORE
                ]
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
def test_is_user_assigned(data, expected_result):
    assigned_users = {"assigned_users": data}
    assert permissions.is_user_assigned(user_id, assigned_users) == expected_result


@pytest.mark.parametrize(
    "data, expected_result",
    (
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": user_id},
                    ]
                },
                "case_officer": {"id": user_id},
            },
            True,
        ),
        (
            {
                "assigned_users": {
                    "fake queue": [
                        {"id": user_id},
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
                "case_officer": {"id": user_id},
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
def test_is_user_case_advisor_or_assigned_user_rule(data, expected_result):
    assert rules.test_rule("is_user_case_advisor_or_assigned_user", user_id, data) == expected_result
