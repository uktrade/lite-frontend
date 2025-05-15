import pytest

from django.urls import reverse
from exporter.applications.forms.hcsat import HCSATminiform
from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup

from core import client


@pytest.fixture
def success_url():
    def _success_url(id):
        return reverse("applications:success_page", kwargs={"pk": id})

    return _success_url


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def survey_id():
    return "6de657c9-e500-4791-8c8b-9f94dec2c629"  # /PS-IGNORE


@pytest.fixture
def siel_application_url(application_pk):
    return reverse("applications:application", kwargs={"pk": application_pk})


@pytest.fixture
def f680_application_url(data_submitted_f680_case):
    return reverse("f680:submitted_summary", kwargs={"pk": data_submitted_f680_case["case"]["id"]})


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
    "case_type_reference, application, application_url, expected_form_title",
    [
        (
            "siel",
            "data_standard_case",
            "siel_application_url",
            "Overall, how would you rate your experience with the 'apply for a standard individual export licence (SIEL)' service today?",
        ),
        (
            "f680",
            "data_submitted_f680_case",
            "f680_application_url",
            "Overall, how would you rate your experience with the 'apply for F680 security approval' service today?",
        ),
    ],
)
def test_success_view(
    authorized_client,
    success_url,
    home_url,
    application_start_url,
    requests_mock,
    case_type_reference,
    application,
    application_url,
    expected_form_title,
    request,
):
    application = request.getfixturevalue(application)
    application["case"]["status"] = application["case"]["data"]["status"]
    application_id = application["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/applications/{application_id}"), json=application["case"])

    response = authorized_client.get(success_url(application_id))

    assert response.status_code == 200

    assert isinstance(response.context["form"], HCSATminiform)
    assert response.context["form"].title == expected_form_title
    assertTemplateUsed(response, "applications/application-submit-success.html")

    soup = BeautifulSoup(response.content, "html.parser")

    # content
    element = soup.find("div", attrs={"data-case_type": True})
    assert element["data-case_type"] == case_type_reference
    assert soup.find("h1").string.strip() == "Application submitted"
    assert soup.find("a", {"class": "govuk-back-link"})["href"] == request.getfixturevalue(application_url)
    assert (
        soup.find("div", {"id": "application-processing-message-value"}).string.strip()
        == "ECJU reference: " + application["case"]["reference_code"]
    )

    # links
    links = soup.findAll("a", {"class": "success-navigation"})
    assert links[0]["href"] == reverse("applications:applications")
    assert links[1]["href"] == application_start_url
    assert links[2]["href"] == home_url

    # form exists
    assert soup.find("input", {"id": "star1"})
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit and continue"


def test_apply_for_licence_start_view(authorized_client, application_start_url):
    response = authorized_client.get(application_start_url)

    assert response.status_code == 200


@pytest.mark.parametrize("application", ["data_standard_case", "data_submitted_f680_case"])
def test_post_survey_feedback(
    authorized_client,
    success_url,
    survey_id,
    mock_post_survey,
    requests_mock,
    application,
    request,
):
    application = request.getfixturevalue(application)
    application_id = application["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/applications/{application_id}"), json=application["case"])

    response = authorized_client.post(success_url(application_id), data={"satisfaction_rating": "NEITHER"})
    assert response.status_code == 302
    assert response.url == reverse("applications:application-hcsat", kwargs={"pk": application_id, "sid": survey_id})
    assert mock_post_survey.called_once
    assert mock_post_survey.last_request.json() == {
        "satisfaction_rating": "NEITHER",
        "user_journey": "APPLICATION_SUBMISSION",
        "case_type": application["case"]["case_type"]["id"],
    }


def test_post_survey_feedback_invalid(authorized_client, success_url, mock_post_survey, application_pk):
    response = authorized_client.post(success_url(application_pk), data={})
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("span", {"class": "govuk-error-message"}).text.strip() == "Error: Star rating is required"

    assert not mock_post_survey.called
