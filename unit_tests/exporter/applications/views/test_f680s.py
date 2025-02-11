import pytest
from uuid import uuid4

from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from exporter.f680.constants import (
    ApplicationFormSteps,
)
from exporter.f680.forms import ApplicationNameForm, ApplicationSubmissionForm


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def f680_apply_url():
    return reverse("f680:apply")


@pytest.fixture
def f680_summary_url_with_application(data_f680_case):
    return reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})


@pytest.fixture
def post_to_step(post_to_step_factory, f680_apply_url, mock_application_post):
    return post_to_step_factory(f680_apply_url)


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_application_post(requests_mock, data_f680_case):
    application = data_f680_case
    url = client._build_absolute_uri(f"/exporter/f680/application/")
    return requests_mock.post(url=url, json=application, status_code=201)


@pytest.fixture()
def set_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


class TestApplyForLicenceQuestionsClass:
    def test_triage_f680_apply_redirect_success(self, authorized_client, f680_apply_url):
        response = authorized_client.post(reverse("apply_for_a_licence:f680_questions"))
        assert response.status_code == 302
        assert response.url == f680_apply_url


class TestF680ApplicationCreateView:
    def test_get_create_f680_view_success(
        self,
        authorized_client,
        f680_apply_url,
        mock_f680_application_get,
        set_f680_feature_flag,
    ):
        response = authorized_client.get(f680_apply_url)

        assert isinstance(response.context["form"], ApplicationNameForm)
        soup = BeautifulSoup(response.content, "html.parser")
        assert "Name of the application" in soup.find("h1").text

    def test_get_create_f680_view_fail_with_feature_flag_off(
        self,
        authorized_client,
        f680_apply_url,
        mock_f680_application_get,
    ):
        response = authorized_client.get(f680_apply_url)
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_post_to_create_f680_name_step_success(
        self,
        authorized_client,
        f680_apply_url,
        post_to_step,
        f680_summary_url_with_application,
        set_f680_feature_flag,
    ):
        response = post_to_step(
            ApplicationFormSteps.APPLICATION_NAME,
            {"name": "F680 Test"},
        )

        assert response.status_code == 302
        assert response.url == f680_summary_url_with_application

    def test_post_to_create_f680_name_step_invalid_data(
        self,
        authorized_client,
        f680_apply_url,
        post_to_step,
        set_f680_feature_flag,
    ):
        response = post_to_step(
            ApplicationFormSteps.APPLICATION_NAME,
            {"name": ""},
        )

        assert isinstance(response.context["form"], ApplicationNameForm)
        assert response.context["form"].errors
        assert response.context["form"].errors.get("name")[0] == "This field is required."


class TestF680ApplicationSummaryView:
    def test_get_f680_summary_view_success(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        set_f680_feature_flag,
    ):
        response = authorized_client.get(f680_summary_url_with_application)

        assert isinstance(response.context["form"], ApplicationSubmissionForm)
        assertTemplateUsed(response, "f680/summary.html")

        content = BeautifulSoup(response.content, "html.parser")
        heading_element = content.find("h1", class_="govuk-heading-l govuk-!-margin-bottom-2")
        assert heading_element.string.strip() == "F680 Application"

    def test_get_f680_summary_view_case_not_found(
        self,
        authorized_client,
        requests_mock,
        set_f680_feature_flag,
    ):

        app_pk = str(uuid4())
        client_uri = client._build_absolute_uri(f"/exporter/f680/application/{app_pk}/")

        requests_mock.get(client_uri, json={}, status_code=404)

        response = authorized_client.get(reverse("f680:summary", kwargs={"pk": app_pk}))
        assert response.status_code == 404

    def test_get_f680_summary_view_fail_with_feature_flag_off(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
    ):
        response = authorized_client.get(f680_summary_url_with_application)
        assert response.status_code == 200
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_post_f680_submission_form_success(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        set_f680_feature_flag,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.status_code == 302
        assert response.url == f680_summary_url_with_application

    def test_post_f680_submission_form_fail_with_feature_flag_off(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )
