import pytest
import re

from bs4 import BeautifulSoup
import rules

from django.urls import reverse

from core import client
from caseworker.tau import views
from core.exceptions import ServiceError


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_regime_entries,
    mock_application_good_documents,
    mock_good_precedent_endpoint_empty,
    mock_mtcr_entries_get,
    mock_wassenaar_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
):
    yield


@pytest.fixture
def edit_multiple_assessments_url(data_standard_case):
    return reverse(
        "cases:tau:multiple_edit",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


def test_edit_multiple_assessments_GET(
    authorized_client,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
):
    response = authorized_client.get(edit_multiple_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Edit assessments"

    table = soup.find("table", id="tau-form")
    assert table
    table_rows = table.select("tbody tr")
    assert len(table_rows) == 2

    def get_td_text(table_row):
        return [td.text.strip().strip() for td in table_row.findAll("td", {"class": "readonly-field"})]

    assert get_td_text(table_rows[0]) == [
        "1.",
        "p1 44",
        "ML1 ML1a",
        "",
        "wassenaar-1 mtcr-1 nsg-1",
        "",
        "test comment",
    ]


def test_edit_multiple_assessments_POST_success(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    tau_assessment_url,
    wassenaar_regime_entry,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 2,
        "form-INITIAL_FORMS": 2,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 2,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": ["ML1", "ML1a"],
        "form-0-licence": True,
        "form-0-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
        "form-1-id": good_on_application_2["id"],
        "form-1-control_list_entries": ["ML1"],
        "form-1-licence": True,
        "form-1-report_summary_prefix": good_on_application_2["report_summary_prefix"]["id"],
        "form-1-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-1-refer_to_ncsc": True,
        "form-1-regimes": [wassenaar_regime_entry["pk"]],
        "form-1-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert mocked_assessment_endpoint.last_request.json() == [
        {
            "control_list_entries": ["ML1", "ML1a"],
            "report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
            "report_summary_prefix": "",
            "comment": "some multiple edit comment",
            "id": good_on_application_1["id"],
            "is_good_controlled": True,
            "regime_entries": [],
            "is_ncsc_military_information_security": False,
        },
        {
            "control_list_entries": ["ML1"],
            "report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
            "report_summary_prefix": good_on_application_2["report_summary_prefix"]["id"],
            "comment": "some multiple edit comment",
            "id": good_on_application_2["id"],
            "is_good_controlled": True,
            "regime_entries": [wassenaar_regime_entry["pk"]],
            "is_ncsc_military_information_security": True,
        },
    ]
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Edited assessments for 2 products."
    assert messages == [expected_message]
    assert response.redirect_chain[-1][0] == tau_assessment_url


def test_edit_multiple_assessments_POST_uncontrolled_with_cle(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": ["ML1", "ML1a"],
        "form-0-licence": False,
        "form-0-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"][0].non_field_errors() == [
        "Control list entries cannot be added for a non-controlled product."
    ]


def test_edit_multiple_assessments_POST_controlled_missing_cle(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": [],
        "form-0-licence": True,
        "form-0-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"][0].non_field_errors() == [
        "Control list entries and report summary subject MUST be selected for a controlled product."
    ]
