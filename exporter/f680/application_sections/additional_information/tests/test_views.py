import pytest

from django.urls import reverse

from core import client

from ..forms import NotesForCaseOfficerForm
from ..constants import FormSteps


@pytest.fixture()
def unset_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture()
def set_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = [organisation_pk]
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture()
def unset_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = ["12345"]
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def missing_application_id():
    return "6bb0828c-1520-4624-b729-7f3e6e5b9f5d"


@pytest.fixture
def missing_f680_application_wizard_url(missing_application_id):
    return reverse(
        "f680:additional_information:notes_wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_application_wizard_url(data_f680_case):
    return reverse(
        "f680:additional_information:notes_wizard",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def mock_f680_application_get_404(requests_mock, missing_application_id):
    url = client._build_absolute_uri(f"/exporter/f680/application/{missing_application_id}/")
    return requests_mock.get(url=url, json={}, status_code=404)


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_f680_application_get_existing_data(requests_mock, data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "notes_for_case_officers": {
                "type": "single",
                "label": "Notes for case officers",
                "fields": [
                    {
                        "key": "note",
                        "answer": "Some note text",
                        "datatype": "string",
                        "question": "Add note",
                        "raw_answer": "Some note text",
                    }
                ],
            }
        }
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_patch_f680_application(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.patch(url=url, json=data_f680_case)


@pytest.fixture
def post_to_step(post_to_step_factory, f680_application_wizard_url):
    return post_to_step_factory(f680_application_wizard_url)


@pytest.fixture
def goto_step(goto_step_factory, f680_application_wizard_url):
    return goto_step_factory(f680_application_wizard_url)


class TestAdditionalInformationView:

    def test_GET_no_application_404(
        self,
        authorized_client,
        missing_f680_application_wizard_url,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(missing_f680_application_wizard_url)
        assert response.status_code == 404

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], NotesForCaseOfficerForm)

    def test_GET_success_with_organisation_set(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], NotesForCaseOfficerForm)

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_GET_no_feature_organisation_allowed(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_POST_approval_type_and_submit_wizard_success(
        self, post_to_step, goto_step, mock_f680_application_get, mock_patch_f680_application
    ):
        response = post_to_step(
            FormSteps.NOTES_FOR_CASEWORKER,
            {"note": "Some information"},
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "notes_for_case_officers": {
                        "label": "Notes for case officers",
                        "fields": [
                            {
                                "key": "note",
                                "answer": "Some information",
                                "raw_answer": "Some information",
                                "question": "Add note",
                                "datatype": "string",
                            }
                        ],
                        "type": "single",
                    }
                },
            }
        }

    def test_POST_to_step_validation_error(
        self,
        post_to_step,
        goto_step,
        mock_f680_application_get,
    ):
        goto_step(FormSteps.NOTES_FOR_CASEWORKER)
        response = post_to_step(
            FormSteps.NOTES_FOR_CASEWORKER,
            {},
        )
        assert response.status_code == 200
        assert response.context["form"]["note"].errors == ["This field is required."]

    def test_GET_with_existing_data_success(
        self,
        authorized_client,
        mock_f680_application_get_existing_data,
        f680_application_wizard_url,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], NotesForCaseOfficerForm)
        assert response.context["form"]["note"].initial == "Some note text"
