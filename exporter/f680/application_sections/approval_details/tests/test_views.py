import pytest

from django.urls import reverse

from core import client

from ..forms import ApprovalTypeForm
from ..constants import FormSteps


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


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def missing_application_id():
    return "6bb0828c-1520-4624-b729-7f3e6e5b9f5d"


@pytest.fixture
def missing_f680_application_wizard_url(missing_application_id):
    return reverse(
        "f680:approval_details:type_wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_application_wizard_url(data_f680_case):
    return reverse(
        "f680:approval_details:type_wizard",
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


class TestApprovalDetailsView:

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
        assert isinstance(response.context["form"], ApprovalTypeForm)

    def test_GET_success_organisation_set(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], ApprovalTypeForm)

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

    def test_GET_no_organisation_allowed(
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
            FormSteps.APPROVAL_TYPE,
            {"approval_choices": ["training", "supply"]},
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "approval_type": {
                        "label": "Approval type",
                        "fields": [
                            {
                                "key": "approval_choices",
                                "answer": ["Training", "Supply"],
                                "raw_answer": ["training", "supply"],
                                "question": "Select the types of approvals you need",
                                "datatype": "list",
                            },
                            {
                                "key": "demonstration_in_uk",
                                "answer": "",
                                "raw_answer": "",
                                "question": "Explain what you are demonstrating and why",
                                "datatype": "string",
                            },
                            {
                                "key": "demonstration_overseas",
                                "answer": "",
                                "raw_answer": "",
                                "question": "Explain what you are demonstrating and why",
                                "datatype": "string",
                            },
                            {
                                "key": "approval_details_text",
                                "answer": "",
                                "raw_answer": "",
                                "question": "Provide details about what you're seeking approval to do",
                                "datatype": "string",
                            },
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
        goto_step(FormSteps.APPROVAL_TYPE)
        response = post_to_step(
            FormSteps.APPROVAL_TYPE,
            {},
        )
        assert response.status_code == 200
        assert "Select an approval choice" in response.context["form"]["approval_choices"].errors

    def test_GET_with_existing_data_success(
        self,
        authorized_client,
        mock_f680_application_get_existing_data,
        f680_application_wizard_url,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], ApprovalTypeForm)
        assert response.context["form"]["approval_choices"].initial == [
            "initial_discussion_or_promoting",
            "demonstration_in_uk",
            "demonstration_overseas",
            "training",
            "through_life_support",
            "supply",
        ]
        assert response.context["form"]["demonstration_in_uk"].initial == "some UK demonstration reason"
        assert response.context["form"]["demonstration_overseas"].initial == "some overseas demonstration reason"
        assert response.context["form"]["approval_details_text"].initial == "some details"
