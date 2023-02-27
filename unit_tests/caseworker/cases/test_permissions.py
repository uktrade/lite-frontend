import pytest
from django.urls import reverse

import rules
from bs4 import BeautifulSoup
from caseworker.core import rules as caseworker_rules
from django.urls import reverse


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_gov_lu_user,
    mock_case,
    mock_standard_case_activity_filters,
    mock_standard_case_activity_system_user,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_on_post_circulation_queue,
):
    pass


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


@pytest.mark.parametrize(
    "id_element_name, is_user_case_advisor, id_element_name_visible",
    (
        ["link-change-status", True, True],
        ["link-change-status", False, False],
        ["link-change-queues", True, True],
        ["link-change-queues", False, False],
        ["link-change-review-date", True, True],
        ["link-change-review-date", False, False],
    ),
)
def test_permission_summary_change_links(
    authorized_client, data_queue, data_standard_case, id_element_name, is_user_case_advisor, id_element_name_visible
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    # We are changing rule here since mocking doesn't seem straight forward
    rules.set_rule("can_user_change_case", lambda: is_user_case_advisor)
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    id_html_find_result = soup.find(id=id_element_name)
    if id_element_name_visible:
        assert id_html_find_result
    else:
        assert id_html_find_result is None
