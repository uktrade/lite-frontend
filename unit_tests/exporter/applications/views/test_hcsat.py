import pytest
from django.urls import reverse
from exporter.applications.forms.hcsat import HCSATApplicationForm
from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup

from core import client


@pytest.fixture
def survey_id():
    return "6de657c9-e500-4791-8c8b-9f94dec2c629"  # /PS-IGNORE


@pytest.fixture
def hcsat_url():
    def _hcsat_url(survey_id, application_id):
        return reverse("applications:application-hcsat", kwargs={"sid": survey_id, "pk": application_id})

    return _hcsat_url


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def siel_application_url(application_pk):
    return reverse("applications:application", kwargs={"pk": application_pk})


@pytest.fixture
def f680_application_url(data_submitted_f680_case):
    return reverse("applications:application", kwargs={"pk": data_submitted_f680_case["case"]["id"]})


@pytest.fixture
def application_start_url():
    return reverse("apply_for_a_licence:start")


@pytest.fixture
def home_url():
    return reverse("core:home")


@pytest.fixture
def application_reference_number(data_standard_case):
    return data_standard_case["case"]["reference_code"]


@pytest.fixture(autouse=True)
def setup(mock_get_application):
    yield


@pytest.mark.parametrize(
    "application, application_url, expected_form_title",
    [
        (
            "data_standard_case",
            "siel_application_url",
            "Overall, how would you rate your experience with the 'apply for a standard individual export licence (SIEL)' service today?",
        ),
        (
            "data_submitted_f680_case",
            "f680_application_url",
            "Overall, how would you rate your experience with the 'apply for F680 security approval' service today?",
        ),
    ],
)
def test_hcsat_view(
    authorized_client,
    hcsat_url,
    mock_get_survey,
    survey_id,
    requests_mock,
    application,
    application_url,
    expected_form_title,
    request,
):
    application = request.getfixturevalue(application)
    application_id = application["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/applications/{application_id}"), json=application["case"])

    url = hcsat_url(survey_id, application_id)
    response = authorized_client.get(url)
    assert response.status_code == 200

    assert isinstance(response.context["form"], HCSATApplicationForm)
    assert response.context["form"].title == expected_form_title
    assertTemplateUsed(response, "applications/hcsat_form.html")

    soup = BeautifulSoup(response.content, "html.parser")

    # content
    assert soup.find("h1").string.strip() == "Give feedback on this service"
    assert soup.find("a", {"class": "govuk-back-link"})["href"] == request.getfixturevalue(application_url)

    # form exists
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit feedback"
    assert soup.find("a", {"class": "govuk-button--secondary"})["href"] == reverse("core:home")

    assert mock_get_survey.called_once


@pytest.mark.parametrize(
    "case_type_reference, application, expected_text",
    [
        (
            "siel",
            "data_standard_case",
            "We've sent your responses to the apply for a standard individual export licence (SIEL) team",
        ),
        (
            "f680",
            "data_submitted_f680_case",
            "We've sent your responses to the apply for F680 security approval team",
        ),
    ],
)
def test_post_survey_feedback(
    authorized_client,
    hcsat_url,
    survey_id,
    mock_update_survey,
    mock_get_survey,
    requests_mock,
    case_type_reference,
    application,
    expected_text,
    request,
):
    application = request.getfixturevalue(application)
    application_id = application["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/applications/{application_id}"), json=application["case"])

    url = hcsat_url(survey_id, application_id)
    response = authorized_client.post(
        url, data={"satisfaction_rating": "NEITHER", "user_journey": "APPLICATION_SUBMISSION"}
    )
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")

    # content
    element = soup.find("div", attrs={"data-case_type": True})
    assert element["data-case_type"] == case_type_reference
    assert soup.find("h1").string.strip() == "Feedback submitted successfully"
    assert soup.find("a", {"class": "govuk-button--start"})["href"] == reverse("core:home")
    element = soup.findAll("p", {"class": "govuk-body"})[-1]
    assert expected_text in element.text.strip()

    assert mock_get_survey.called_once

    assert mock_update_survey.called_once
    assert mock_update_survey.last_request.json() == {
        "id": survey_id,
        "user_journey": "APPLICATION_SUBMISSION",
        "satisfaction_rating": None,
        "experienced_issues": [],
        "guidance_application_process_helpful": "",
        "other_detail": "",
        "service_improvements_feedback": "",
        "process_of_creating_account": "",
    }


def test_post_survey_feedback_invalid(
    authorized_client, application_pk, survey_id, hcsat_url, mock_get_survey, mock_update_survey
):
    url = hcsat_url(survey_id, application_pk)
    response = authorized_client.post(url, data={})

    assert response.status_code == 200
    assert mock_get_survey.called_once
    assert not mock_update_survey.called
