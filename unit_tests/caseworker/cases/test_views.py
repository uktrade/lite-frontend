from django.urls import reverse

import pytest


def test_case_audit_trail_system_user(authorized_client, mock_case, mock_queue, mock_case_activity_system_user):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": mock_queue["id"], "pk": mock_case["case"]["id"]})

    # when the case is viewed
    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200


# `goods` for SIEL and it's ilk, goods_type for OIEL and it's ilk
@pytest.mark.parametrize("good_param", ("goods", "goods_types"))
@pytest.mark.parametrize(
    "data,expected",
    (
        # all field present, nothing special
        (
            {
                "comment": "Some comment",
                "control_list_entries[]": ["ML1a"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
            {
                "objects": ["some-good-id"],
                "comment": "Some comment",
                "control_list_entries": ["ML1a"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
        ),
        # multiple control list entries
        (
            {
                "comment": "Some comment",
                "control_list_entries[]": ["ML1a", "ML1"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
            {
                "objects": ["some-good-id"],
                "comment": "Some comment",
                "control_list_entries": ["ML1a", "ML1"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
        ),
        # no comment
        (
            {
                "comment": "",
                "control_list_entries[]": ["ML1a"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
            {
                "objects": ["some-good-id"],
                "comment": "",
                "control_list_entries": ["ML1a"],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
        ),
        # not controlled and no control list entries
        (
            {
                "comment": "Some comment",
                "control_list_entries[]": [],
                "is_good_controlled": False,
                "report_summary": "some-report-summary-id",
            },
            {
                "objects": ["some-good-id"],
                "comment": "Some comment",
                "control_list_entries": [],
                "is_good_controlled": False,
                "report_summary": "some-report-summary-id",
            },
        ),
        # is controlled but no control list entries
        (
            {
                "comment": "Some comment",
                "control_list_entries[]": [],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
            {
                "objects": ["some-good-id"],
                "comment": "Some comment",
                "control_list_entries": [],
                "is_good_controlled": True,
                "report_summary": "some-report-summary-id",
            },
        ),
    ),
)
def test_review_goods(
    authorized_client, requests_mock, mock_queue, mock_case, mock_control_list_entries, data, expected, good_param
):
    case_pk = mock_case["case"]["id"]
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{case_pk}/", json={})

    url = reverse("cases:review_goods", kwargs={"queue_pk": mock_queue["id"], "pk": case_pk})
    response = authorized_client.post(f"{url}?{good_param}=some-good-id", data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == expected
