import pytest
from uuid import uuid4

from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from exporter.f680.forms import ApplicationSubmissionForm


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def f680_apply_url():
    return reverse("f680:apply")


@pytest.fixture
def data_f680_case(data_organisation):
    return {
        "id": "6cf7b401-62dc-4577-ad1d-4282f2aabc96",
        "application": {"name": "F680 Test 1"},
        "reference_code": None,
        "organisation": {
            "id": "3913ff20-5a2b-468a-bf5d-427228459b06",
            "name": "Archway Communications",
            "type": "commercial",
            "status": "active",
        },
        "submitted_at": None,
        "submitted_by": None,
    }


@pytest.fixture
def data_f680_case_complete_application(data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {},
            "approval_type": {},
            "user_information": {},
            "product_information": {},
        }
    }
    return data_f680_case


@pytest.fixture
def data_f680_case_partially_complete_application(data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {},
            "user_information": {},
        }
    }
    return data_f680_case


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
def mock_f680_application_get_application_complete(requests_mock, data_f680_case_complete_application):
    application_id = data_f680_case_complete_application["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case_complete_application)


@pytest.fixture
def mock_f680_application_get_application_partially_complete(
    requests_mock, data_f680_case_partially_complete_application
):
    application_id = data_f680_case_partially_complete_application["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case_partially_complete_application)


@pytest.fixture
def mock_application_post(requests_mock, data_f680_case):
    application = data_f680_case
    url = client._build_absolute_uri(f"/exporter/f680/application/")
    return requests_mock.post(url=url, json=application, status_code=201)


@pytest.fixture
def mock_f680_application_submit(requests_mock, data_f680_case_complete_application):
    application_id = data_f680_case_complete_application["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/submit/")
    return requests_mock.post(url=url, json=data_f680_case_complete_application)


@pytest.fixture()
def unset_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture()
def unset_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = ["12345"]
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture()
def set_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = [organisation_pk]
    settings.FEATURE_FLAG_ALLOW_F680 = False


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
        f680_summary_url_with_application,
        mock_application_post,
    ):
        response = authorized_client.get(f680_apply_url)
        assert response.status_code == 302
        assert response.url == f680_summary_url_with_application
        assert mock_application_post.called_once
        assert mock_application_post.last_request.json() == {"application": {}}

    def test_get_create_f680_view_success_allowed_organisation(
        self,
        authorized_client,
        f680_apply_url,
        f680_summary_url_with_application,
        mock_application_post,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_apply_url)
        assert response.status_code == 302
        assert response.url == f680_summary_url_with_application
        assert mock_application_post.called_once
        assert mock_application_post.last_request.json() == {"application": {}}

    def test_get_create_f680_view_fail_with_feature_flag_off(
        self,
        authorized_client,
        f680_apply_url,
        mock_f680_application_get,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_apply_url)
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_get_create_f680_view_fail_with_feature_organidation_not_allowed(
        self,
        authorized_client,
        f680_apply_url,
        mock_f680_application_get,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_apply_url)
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )


class TestF680ApplicationSummaryView:
    def test_get_f680_summary_view_success(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
    ):
        response = authorized_client.get(f680_summary_url_with_application)

        assert isinstance(response.context["form"], ApplicationSubmissionForm)
        assertTemplateUsed(response, "f680/summary.html")

        content = BeautifulSoup(response.content, "html.parser")
        heading_element = content.find("h1", class_="govuk-heading-l govuk-!-margin-bottom-2")
        assert heading_element.string.strip() == "F680 Application"

    def test_get_f680_summary_view_success_organisation_allowed(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        set_f680_allowed_organisation,
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
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_summary_url_with_application)
        assert response.status_code == 200
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_get_f680_summary_view_fail_with_feature_organisation_not_allowed(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_summary_url_with_application)
        assert response.status_code == 200
        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_post_f680_submission_form_missing_all_sections_returns_errors(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.status_code == 200
        assert response.context["errors"] == {"missing_sections": ["Please complete all required sections"]}

    def test_post_f680_submission_form_partially_complete_returns_errors(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get_application_partially_complete,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.status_code == 200
        assert response.context["errors"] == {"missing_sections": ["Please complete all required sections"]}

    def test_post_f680_submission_form_success(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get_application_complete,
        mock_f680_application_submit,
        data_f680_case_complete_application,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.status_code == 302
        assert response.url == reverse(
            "applications:success_page", kwargs={"pk": data_f680_case_complete_application["id"]}
        )

    def test_post_f680_submission_form_fail_with_feature_flag_off(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        unset_f680_feature_flag,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )

    def test_post_f680_submission_form_fail_with_organisation_not_allowed(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.post(
            f680_summary_url_with_application,
        )

        assert response.context[0].get("title") == "Forbidden"
        assert (
            "You are not authorised to use the F680 Security Clearance application feature"
            in response.context[0].get("description").args
        )
