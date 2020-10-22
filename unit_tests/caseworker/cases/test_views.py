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


def test_case_audit_trail_system_user(authorized_client, open_case_pk, queue_pk):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    # when the case is viewed
    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200


good_review_parametrize_data = (
    # all field present, nothing special
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
        },
        {
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
            "control_list_entries": ["ML1a", "ML1"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
        },
        {
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
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
        },
        {
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
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": False,
            "report_summary": "some-report-summary-id",
        },
        {
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
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
        },
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
        },
    ),
)


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_standard_review_goods(
    authorized_client, requests_mock, standard_case_pk, queue_pk, data, expected, data_standard_case
):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{standard_case_pk}/", json={})
    good_pk = data_standard_case["case"]["data"]["goods"][0]["good"]["id"]
    step_data = build_wizard_step_data(
        view_name="review_standard_application_good_wizard_view", step_name=good_pk, data=data,
    )
    url = reverse("cases:review_standard_application_goods", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})

    response = authorized_client.get(f"{url}?goods={good_pk}")

    assert response.status_code == 200

    response = authorized_client.post(f"{url}?goods={good_pk}", step_data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected, "objects": [good_pk]}


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_open_review_goods(authorized_client, requests_mock, open_case_pk, queue_pk, data, expected, data_open_case):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{open_case_pk}/", json={})
    good_pk = data_open_case["case"]["data"]["goods_types"][0]["id"]
    step_data = build_wizard_step_data(
        view_name="review_open_application_good_wizard_view", step_name=good_pk, data=data,
    )
    url = reverse("cases:review_open_application_goods", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    response = authorized_client.get(f"{url}?goods_types={good_pk}")

    assert response.status_code == 200

    response = authorized_client.post(f"{url}?goods_types={good_pk}", step_data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected, "objects": [good_pk]}


def build_wizard_step_data(view_name, step_name, data):
    step_data = {f"{view_name}-current_step": step_name}
    step_data.update({f"{step_name}-{key}": value for key, value in data.items()})
    return step_data


def test_good_on_application_detail(
    authorized_client,
    mock_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_search,
    data_good_on_application,
    data_standard_case,
):
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same part number and control list entries
    assert mock_search.request_history[0].qs == {"part": ["44"], "clc_rating": ["ml1", "ml2"]}
    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == data_good_on_application
    assert response.context_data["other_cases"] == data_search
    assert response.context_data["case"] == data_standard_case["case"]
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'part:"44" clc_rating:"ML1" clc_rating:"ML2"'


def test_good_on_application_detail_no_part_number(
    authorized_client, mock_search, queue_pk, standard_case_pk, good_on_application_pk, data_good_on_application,
):
    # given I access good on application details for a good with control list entries but no part number
    data_good_on_application["good"]["part_number"] = ""
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same control list entries
    assert mock_search.request_history[0].qs == {"clc_rating": ["ml1", "ml2"]}
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1" clc_rating:"ML2"'


def test_good_on_application_detail_no_part_number_no_control_list_entries(
    authorized_client, mock_search, queue_pk, standard_case_pk, good_on_application_pk, data_good_on_application,
):
    # given I access good on application details for a good with neither part number of control list entries
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["control_list_entries"] = []
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is not requested
    assert len(mock_search.request_history) == 0
    # and the form is left blank
    assert response.context_data["form"]["search_string"].initial == ""


def test_good_on_application_detail_not_rated_at_application_level(
    authorized_client, mock_search, queue_pk, standard_case_pk, good_on_application_pk, data_good_on_application,
):
    # given I access good on application details for a good that has not been rated at application level
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["good"]["control_list_entries"] = ({"rating": "ML1", "text": "Smooth-bore..."},)
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same control list entries as canonical good
    assert mock_search.request_history[0].qs == {"clc_rating": ["ml1"]}
    # and the form is pre-populated with the canonical good control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1"'
