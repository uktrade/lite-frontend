import pytest
import rules

from caseworker.core import rules as caseworker_rules

mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"


@pytest.mark.parametrize(
    "data, expected_result",
    (
        ({"case_officer": {"id": "00c341d1-d83e-4a12-b103-c3fb575a5962"}}, False),  # /PS-IGNORE
        ({"case_officer": {"id": mock_gov_user_id}}, True),
        ({"case_officer": None}, False),
    ),
)
def test_is_user_case_officer(data, mock_gov_user, expected_result):
    assert caseworker_rules.is_user_case_adviser(mock_gov_user["user"], data) == expected_result


def test_is_user_case_officer_none():
    assert caseworker_rules.is_user_case_adviser(None, {"case_officer": None}) == False


@pytest.mark.parametrize(
    "data, expected_result",
    (
        (
            {
                "fake queue": [
                    {"id": mock_gov_user_id},
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
def test_is_user_assigned(data, mock_gov_user, expected_result):
    assigned_users = {"assigned_users": data}
    assert caseworker_rules.is_user_assigned(mock_gov_user["user"], assigned_users) == expected_result


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
def test_can_user_change_case(data, mock_gov_user, expected_result):
    assert rules.test_rule("can_user_change_case", mock_gov_user["user"], data) == expected_result
