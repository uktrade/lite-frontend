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
def mock_f680_application_get_existing_data(requests_mock, data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "approval_type": {
                "type": "single",
                "label": "Approval type",
                "fields": [
                    {
                        "key": "approval_choices",
                        "answer": [
                            "Initial discussions or promoting products",
                            "Demonstration in the United Kingdom to overseas customers",
                            "Demonstration overseas",
                            "Training",
                            "Through life support",
                            "Supply",
                        ],
                        "datatype": "list",
                        "question": "Select the types of approvals you need",
                        "raw_answer": [
                            "initial_discussion_or_promoting",
                            "demonstration_in_uk",
                            "demonstration_overseas",
                            "training",
                            "through_life_support",
                            "supply",
                        ],
                    },
                    {
                        "key": "demonstration_in_uk",
                        "answer": "some UK demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some UK demonstration reason",
                    },
                    {
                        "key": "demonstration_overseas",
                        "answer": "some overseas demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some overseas demonstration reason",
                    },
                    {
                        "key": "approval_details_text",
                        "answer": "some details",
                        "datatype": "string",
                        "question": "Provide details about what you're seeking approval to do",
                        "raw_answer": "some details",
                    },
                ],
            },
            "product_information": {
                "label": "Product information",
                "fields": [
                    {
                        "key": "product_name",
                        "answer": "Test Info",
                        "raw_answer": "Test Info",
                        "question": "Give the item a descriptive name",
                        "datatype": "string",
                    },
                    {
                        "key": "product_description",
                        "answer": "It does things",
                        "raw_answer": "It does things",
                        "question": "Describe the item",
                        "datatype": "string",
                    },
                    {
                        "key": "is_foreign_tech_or_information_shared",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Will any foreign technology or information be shared with the item?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "is_controlled_under_itar",
                        "answer": "Yes, it's controlled under  ITAR",
                        "raw_answer": True,
                        "question": "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "controlled_info",
                        "answer": "It just is",
                        "raw_answer": "It just is",
                        "question": "Explain how the technology or information is controlled.Include countries classification levels and reference numbers.  You can upload supporting documents later in your application",
                        "datatype": "string",
                    },
                    {
                        "key": "controlled_information",
                        "answer": "Some info",
                        "raw_answer": "Some info",
                        "question": "What is the ITAR controlled technology or information?",
                        "datatype": "string",
                    },
                    {
                        "key": "itar_reference_number",
                        "answer": "123456",
                        "raw_answer": "123456",
                        "question": "ITAR reference number",
                        "datatype": "string",
                    },
                    {
                        "key": "usml_categories",
                        "answer": "cat 1",
                        "raw_answer": "cat 1",
                        "question": "What are the United States Munitions List (USML) categories listed on your ITAR approval?",
                        "datatype": "string",
                    },
                    {
                        "key": "itar_approval_scope",
                        "answer": "no scope",
                        "raw_answer": "no scope",
                        "question": "Describe the scope of your ITAR approval",
                        "datatype": "string",
                    },
                    {
                        "key": "expected_time_in_possession",
                        "answer": "10 years",
                        "raw_answer": "10 years",
                        "question": "How long do you expect the technology or information that is controlled under the US ITAR to be in your possession?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_including_cryptography_or_security_features",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Does the item include cryptography or other information security features?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "cryptography_or_security_feature_info",
                        "answer": "some",
                        "raw_answer": "some",
                        "question": "Provide full details",
                        "datatype": "string",
                    },
                    {
                        "key": "is_item_rated_under_mctr",
                        "answer": "Yes, the product is MTCR Category 1",
                        "raw_answer": "mtcr_1",
                        "question": "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
                        "datatype": "string",
                    },
                    {
                        "key": "is_item_manpad",
                        "answer": "No, the product is not a MANPAD",
                        "raw_answer": "no",
                        "question": "Do you believe the item is a man-portable air defence system (MANPAD)?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_mod_electronic_data_shared",
                        "answer": "No",
                        "raw_answer": "no",
                        "question": "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?",
                        "datatype": "string",
                    },
                    {
                        "key": "funding_source",
                        "answer": "MOD",
                        "raw_answer": "mod",
                        "question": "Who is funding the item?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_used_by_uk_armed_forces",
                        "answer": "No",
                        "raw_answer": False,
                        "question": "Will the item be used by the UK Armed Forces?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "used_by_uk_armed_forces_info",
                        "answer": "",
                        "raw_answer": "",
                        "question": "Explain how it will be used",
                        "datatype": "string",
                    },
                ],
                "type": "single",
            },
        }
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


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

    def test_post_f680_submission_form_missing_sections_returns_errors(
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

    def test_post_f680_submission_form_success_organisation_allowed(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
        set_f680_allowed_organisation,
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
