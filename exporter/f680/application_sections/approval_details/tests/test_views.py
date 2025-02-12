import pytest

from django.urls import reverse

from core import client

from ..forms import ApprovalTypeForm
from ..constants import FormSteps


@pytest.fixture()
def unset_f680_feature_flag(settings):
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
        "approval_details": {
            "answers": {
                "approval_choices": [
                    "initial_discussion_or_promoting",
                    "demonstration_in_uk",
                    "demonstration_overseas",
                    "training",
                    "through_life_support",
                    "supply",
                ],
                "demonstration_in_uk": "Test text 1",
                "demonstration_overseas": "Test text 2",
            },
            "questions": {
                "approval_choices": None,
                "demonstration_in_uk": "Explain what you are demonstrating and why",
                "demonstration_overseas": "Explain what you are demonstrating and why",
            },
        },
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
                "approval_details": {
                    "answers": {
                        "approval_choices": ["training", "supply"],
                        "demonstration_in_uk": "",
                        "demonstration_overseas": "",
                        "approval_details_text": "",
                    },
                    "questions": {
                        "approval_choices": None,
                        "demonstration_in_uk": "Explain what you are demonstrating and why",
                        "demonstration_overseas": "Explain what you are demonstrating and why",
                        "approval_details_text": "Provide details about what you're seeking approval to do",
                    },
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
        assert response.context["form"]["demonstration_in_uk"].initial == "Test text 1"
        assert response.context["form"]["demonstration_overseas"].initial == "Test text 2"
