import pytest
from uuid import uuid4

from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from exporter.f680.forms import ApplicationPresubmissionForm, ApplicationSubmissionForm


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def apply_for_a_licence_url():
    return reverse("apply_for_a_licence:start")


@pytest.fixture
def data_f680_case_complete_application(data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {},
            "approval_type": {},
            "user_information": {},
            "product_information": {},
        },
    }
    return data_f680_case


@pytest.fixture
def data_f680_case_complete_application_agree_to_foi(data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {},
            "approval_type": {},
            "user_information": {},
            "product_information": {},
        },
        "agreed_to_foi": False,
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
def data_f680_case_application_history(data_f680_case):

    return {
        "id": data_f680_case["id"],
        "reference_code": data_f680_case["reference_code"],
        "amendment_history": [
            {
                "ecju_query_count": 0,
                "reference_code": "F680/2025/0000001",
                "submitted_at": "2025-03-27T16:02:16.695411Z",
                "id": data_f680_case["id"],
                "status": {"status": "submitted", "status_display": "Submitted"},
            }
        ],
    }


@pytest.fixture
def f680_summary_url_with_application(data_f680_case):
    return reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})


@pytest.fixture
def f680_declaration_url_with_application(data_f680_case):
    return reverse("f680:declaration", kwargs={"pk": data_f680_case["id"]})


@pytest.fixture
def f680_submitted_application_summary_url_with_application(data_f680_case_complete_application):
    return reverse("f680:submitted_summary", kwargs={"pk": data_f680_case_complete_application["id"]})


@pytest.fixture
def f680_submitted_application_summary_url_with_application_case_notes(data_f680_case_complete_application):
    return reverse(
        "f680:submitted_summary", kwargs={"pk": data_f680_case_complete_application["id"], "type": "case-notes"}
    )


@pytest.fixture
def f680_submitted_application_summary_url_with_application_ecju_query(data_f680_case_complete_application):
    return reverse(
        "f680:submitted_summary", kwargs={"pk": data_f680_case_complete_application["id"], "type": "ecju-queries"}
    )


@pytest.fixture
def f680_submitted_application_summary_url_with_application_ecju_documents(data_f680_case_complete_application):
    return reverse(
        "f680:submitted_summary",
        kwargs={"pk": data_f680_case_complete_application["id"], "type": "generated-documents"},
    )


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
def mock_f680_application_get_submitted_application(requests_mock, data_f680_submitted_application):
    application_id = data_f680_submitted_application["id"]
    url = client._build_absolute_uri(f"/applications/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_submitted_application)


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
    return requests_mock.post(url=url, json={})


@pytest.fixture
def mock_post_f680_application_declaration(requests_mock, data_f680_case_complete_application_agree_to_foi):
    application_id = data_f680_case_complete_application_agree_to_foi["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/declaration/")
    return requests_mock.post(url=url, json=data_f680_case_complete_application_agree_to_foi)


@pytest.fixture
def mock_patch_f680_application(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.patch(url=url, json=data_f680_case)


@pytest.fixture
def mock_f680_application_get_submitted_application(requests_mock, data_f680_submitted_application):
    application_id = data_f680_submitted_application["id"]
    url = client._build_absolute_uri(f"/applications/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_submitted_application)


@pytest.fixture
def mock_get_application_history(requests_mock, data_f680_submitted_application, data_f680_case_application_history):
    application_id = data_f680_submitted_application["id"]
    url = client._build_absolute_uri(f"/exporter/applications/{application_id}/history")
    return requests_mock.get(url=url, json=data_f680_case_application_history, status_code=200)


@pytest.fixture
def mock_get_f680_case_notes(data_f680_case, requests_mock):
    return requests_mock.get(
        f"/cases/{data_f680_case['id']}/case-notes/",
        json={"case_notes": []},
    )


@pytest.fixture
def mock_get_f680_ecju_queries(data_f680_case, requests_mock):
    return requests_mock.get(
        f"/cases/{data_f680_case['id']}/ecju-queries/",
        json={"ecju_queries": []},
    )


@pytest.fixture
def mock_get_f680_ecju_documents(data_f680_case, requests_mock):
    return requests_mock.get(
        f"/cases/{data_f680_case['id']}/generated-documents/",
        json={"count": 0, "total_pages": 1, "results": []},
    )


def get_activity(request, pk):
    data = client.get(request, f"/applications/{pk}/activity/")
    return data.json()["activity"]


@pytest.fixture
def mock_get_application_activity(requests_mock, data_f680_submitted_application):
    application_id = data_f680_submitted_application["id"]
    url = client._build_absolute_uri(f"/applications/{application_id}/activity/")
    return requests_mock.get(url=url, json={"activity": {}}, status_code=200)


@pytest.fixture
def mock_post_case_notes(requests_mock, data_f680_case):
    return requests_mock.post(
        f"/cases/{data_f680_case['id']}/case-notes/",
        json={},
        status_code=201,
    )


@pytest.fixture
def mock_post_case_notes_error(requests_mock, data_f680_case):
    return requests_mock.post(
        f"/cases/{data_f680_case['id']}/case-notes/",
        json={},
        status_code=500,
    )


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


class TestF680ApplyForALicence:
    def test_POST_apply_for_a_licence_success(
        self,
        authorized_client,
        apply_for_a_licence_url,
        f680_summary_url_with_application,
        mock_application_post,
    ):
        response = authorized_client.post(apply_for_a_licence_url, data={"licence_type": "f680"})
        assert response.status_code == 302
        assert response.url == f680_summary_url_with_application
        assert mock_application_post.called_once
        assert mock_application_post.last_request.json() == {"application": {}}


class TestF680ApplicationSummaryView:
    def test_get_f680_summary_view_success(
        self,
        authorized_client,
        f680_summary_url_with_application,
        mock_f680_application_get,
    ):
        response = authorized_client.get(f680_summary_url_with_application)
        assert isinstance(response.context["form"], ApplicationPresubmissionForm)
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

        assert isinstance(response.context["form"], ApplicationPresubmissionForm)
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
        assert response.url == reverse("f680:declaration", kwargs={"pk": data_f680_case_complete_application["id"]})

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


class TestF680ApplicationDeclarationView:
    def test_GET_f680_declaration_view_success(
        self,
        authorized_client,
        f680_declaration_url_with_application,
        mock_f680_application_get,
        f680_summary_url_with_application,
    ):

        response = authorized_client.get(f680_declaration_url_with_application)

        assert isinstance(response.context["form"], ApplicationSubmissionForm)
        assertTemplateUsed(response, "core/form.html")

        soup = BeautifulSoup(response.content, "html.parser")
        assert soup.find("h1").string == "Submit your application"
        assert soup.find("a", {"id": "back-link"})["href"] == f680_summary_url_with_application
        assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Accept and submit"

    @pytest.mark.parametrize(
        "data, expected_error",
        (
            ({}, "If you agree to make the application details publicly available click yes"),
            (
                {
                    "agreed_to_foi": True,
                },
                "Non disclosure explanation cannot be blank",
            ),
        ),
    )
    def test_POST_f680_declaration_view_fail(
        self,
        authorized_client,
        f680_declaration_url_with_application,
        data,
        expected_error,
        mock_f680_application_get,
    ):

        response = authorized_client.post(f680_declaration_url_with_application, data)
        soup = BeautifulSoup(response.content, "html.parser")
        assert expected_error in soup.find("div", {"class": "govuk-error-summary__body"}).text

    def test_POST_f680_declaration_view_success(
        self,
        authorized_client,
        f680_declaration_url_with_application,
        mock_f680_application_get_application_complete,
        mock_f680_application_submit,
        data_f680_case,
    ):
        response = authorized_client.post(
            f680_declaration_url_with_application, data={"agreed_to_foi": True, "foi_reason": "some reason"}
        )

        assert mock_f680_application_submit.called_once
        assert mock_f680_application_submit.last_request.json() == {"agreed_to_foi": True, "foi_reason": "some reason"}
        assert response.status_code == 302
        assert response.url == reverse("applications:success_page", kwargs={"pk": data_f680_case["id"]})


class TestF680SubmittedApplicationSummaryView:
    def test_get_f680_summary_view_success(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
    ):
        response = authorized_client.get(f680_submitted_application_summary_url_with_application)
        assert response.context["application_sections"] == data_f680_submitted_application["application"]["sections"]

        assert response.status_code == 200

    def test_get_f680_summary_view_success_case_notes(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application_case_notes,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
        mock_get_f680_case_notes,
    ):
        application_id = data_f680_submitted_application["id"]

        response = authorized_client.get(f680_submitted_application_summary_url_with_application_case_notes)
        content = BeautifulSoup(response.content, "html.parser")
        case_notes_title = content.find("label", {"id": "case-notes-title"}).text
        return_url = content.find("a", {"id": "case-notes-return-url"}).get("href")

        assert response.status_code == 200
        assert case_notes_title == "Add a note"
        assert return_url == f"/f680/{application_id}/summary/"

    def test_get_f680_summary_view_success_ecju_queries(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application_ecju_query,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
        mock_get_f680_ecju_queries,
    ):

        response = authorized_client.get(f680_submitted_application_summary_url_with_application_ecju_query)
        content = BeautifulSoup(response.content, "html.parser")

        queries_text = content.find("p", {"id": "queries-info"}).text

        assert response.status_code == 200
        assert "There are no ECJU queries on this application." in queries_text

    def test_get_f680_summary_view_success_ecju_documents(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application_ecju_documents,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
        mock_get_f680_ecju_documents,
    ):

        response = authorized_client.get(f680_submitted_application_summary_url_with_application_ecju_documents)
        content = BeautifulSoup(response.content, "html.parser")
        document_info_text = content.find("p", {"id": "documents-info"}).text

        assert response.status_code == 200
        assert "There are no ECJU documents for this product." in document_info_text

    def test_post_f680_summary_view_success_case_notes(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application_case_notes,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
        mock_get_f680_case_notes,
        mock_post_case_notes,
    ):
        application_id = data_f680_submitted_application["id"]

        note_json = {"text": "Note text"}

        post_response = authorized_client.post(
            f680_submitted_application_summary_url_with_application_case_notes, data=note_json
        )

        assert mock_post_case_notes.last_request.json() == {"text": "Note text"}
        assert post_response.status_code == 302
        assert post_response.url == f"/f680/{application_id}/summary/case-notes/"

    def test_post_f680_summary_view_case_notes_with_wrong_type_raises_404(
        self,
        authorized_client,
        f680_submitted_application_summary_url_with_application_ecju_documents,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        data_f680_submitted_application,
        mock_get_f680_case_notes,
        mock_post_case_notes,
    ):

        note_json = {"text": "Note text"}

        post_response = authorized_client.post(
            f680_submitted_application_summary_url_with_application_ecju_documents, data=note_json
        )

        assert post_response.status_code == 404

    def test_post_case_notes_error(
        self,
        authorized_client,
        requests_mock,
        data_f680_submitted_application,
        f680_submitted_application_summary_url_with_application_case_notes,
        mock_f680_application_get_submitted_application,
        mock_get_application_history,
        mock_get_application_activity,
        mock_get_f680_case_notes,
        mock_post_case_notes_error,
    ):

        app_pk = data_f680_submitted_application["id"]

        response = authorized_client.post(
            reverse("f680:submitted_summary", kwargs={"pk": app_pk, "type": "case-notes"})
        )

        content = BeautifulSoup(response.content, "html.parser")
        error_text = content.find("p", {"class": "govuk-body"}).text

        assert response.status_code == 200
        assert "Unexpected error creating case note" in error_text
