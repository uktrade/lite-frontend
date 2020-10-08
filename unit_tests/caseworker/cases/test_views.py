from django.urls import reverse

import pytest


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case_activity_system_user,
    mock_case,
    mock_control_list_entries,
    mock_search,
    mock_good_on_appplication,
):
    yield


def test_case_audit_trail_system_user(authorized_client, case_pk, queue_pk):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": case_pk})

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
def test_review_goods(authorized_client, requests_mock, case_pk, queue_pk, data, expected, good_param):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{case_pk}/", json={})

    url = reverse("cases:review_goods", kwargs={"queue_pk": queue_pk, "pk": case_pk})
    response = authorized_client.post(f"{url}?{good_param}=some-good-id", data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == expected


def test_good_on_application_detail(
    authorized_client,
    mock_search,
    queue_pk,
    case_pk,
    good_on_application_pk,
    data_search,
    data_good_on_application,
    data_case,
):
    # given I access good on application details for a good with control list entries
    url = reverse("cases:good", kwargs={"queue_pk": queue_pk, "pk": case_pk, "good_pk": good_on_application_pk})
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same part number and control list entries
    assert mock_search.request_history[0].qs == {"part": ["44"], "clc_rating": ["ml1", "ml2"]}
    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == data_good_on_application
    assert response.context_data["other_cases"] == data_search
    assert response.context_data["case"] == data_case["case"]
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'part:"44" clc_rating:"ML1" clc_rating:"ML2"'
