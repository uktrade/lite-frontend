import pytest
from datetime import datetime, timedelta

from django.urls import reverse
from freezegun import freeze_time

from core import client

from exporter.f680.application_sections.general_application_details.forms import (
    ApplicationNameForm,
    PreviousApplicationConfirm,
    PreviousApplicationsForm,
    ExceptionalCircumstancesForm,
    ExplainExceptionalCircumstancesForm,
)
from exporter.f680.application_sections.general_application_details.constants import FormSteps


DATETIME_10_DAYS_AGO = datetime.now() - timedelta(days=10)
DATETIME_IN_1_YEAR = datetime.now() + timedelta(days=365)


@pytest.fixture()
def unset_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture()
def unset_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = ["12345"]
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture()
def set_f680_allowed_organisation(settings, organisation_pk):
    settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = [organisation_pk]
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture
def missing_application_id():
    return "6bb0828c-1520-4624-b729-7f3e6e5b9f5d"


@pytest.fixture
def missing_f680_application_wizard_url(missing_application_id):
    return reverse(
        "f680:general_application_details:wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_application_wizard_url(data_f680_case):
    return reverse(
        "f680:general_application_details:wizard",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def force_exceptional_circumstances(goto_step, post_to_step):
    goto_step(FormSteps.EXCEPTIONAL_CIRCUMSTANCES)
    post_to_step(
        FormSteps.EXCEPTIONAL_CIRCUMSTANCES,
        {"is_exceptional_circumstances": True},
    )


@pytest.fixture
def force_has_made_previous_application(goto_step, post_to_step):
    goto_step(FormSteps.HAS_MADE_PREVIOUS_APPLICATION)
    post_to_step(
        FormSteps.HAS_MADE_PREVIOUS_APPLICATION,
        {"has_made_previous_application": True},
    )


@pytest.fixture
def mock_f680_application_get_existing_data(requests_mock, data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {
                "label": "General application details",
                "type": "single",
                "fields": {
                    "name": {
                        "key": "name",
                        "answer": "my first F680",
                        "raw_answer": "my first F680",
                        "question": "What is the name of the application?",
                        "datatype": "string",
                    },
                    "previous_application_ecju_reference": {
                        "key": "previous_application_ecju_reference",
                        "answer": "123456",
                        "raw_answer": "123456",
                        "question": "What is the ECJU reference number?",
                        "datatype": "string",
                    },
                    "previous_application_details": {
                        "key": "previous_application_details",
                        "answer": "some info",
                        "raw_answer": "some info",
                        "question": "Can you provide more detail?",
                        "datatype": "string",
                    },
                    "is_exceptional_circumstances": {
                        "key": "is_exceptional_circumstances",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Are there exceptional circumstances?",
                        "datatype": "boolean",
                    },
                    "exceptional_circustances_date": {
                        "key": "exceptional_circumstances_date",
                        "answer": "2090-01-01",
                        "raw_answer": "2090-01-01",
                        "question": "What date do you need it?",
                        "datatype": "date",
                    },
                    "exceptional_circumstances_reason": {
                        "key": "exceptional_circumstances_reason",
                        "answer": "some reason",
                        "raw_answer": "some reason",
                        "question": "What makes the circumstances exceptional?",
                        "datatype": "string",
                    },
                },
                "fields_sequence": [
                    "name",
                    "previous_application_ecju_reference",
                    "previous_application_details",
                    "is_exceptional_circumstances",
                    "exceptional_circumstances_date",
                    "exceptional_circumstances_reason",
                ],
            },
        }
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def post_to_step(post_to_step_factory, f680_application_wizard_url):
    return post_to_step_factory(f680_application_wizard_url)


@pytest.fixture
def goto_step(goto_step_factory, f680_application_wizard_url):
    return goto_step_factory(f680_application_wizard_url)


class TestGeneralApplicationDetailsView:

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
        assert isinstance(response.context["form"], ApplicationNameForm)

    def test_GET_success_organisation_set(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_application_wizard_url,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_application_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], ApplicationNameForm)

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

    @pytest.mark.parametrize(
        "step, data, expected_next_form",
        (
            (FormSteps.APPLICATION_NAME, {"name": "some application name"}, PreviousApplicationConfirm),
            (
                FormSteps.HAS_MADE_PREVIOUS_APPLICATION,
                {"has_made_previous_application": True},
                PreviousApplicationsForm,
            ),
            (
                FormSteps.PREVIOUS_APPLICATION,
                {"previous_application_ecju_reference": "123", "previous_application_details": "some info"},
                ExceptionalCircumstancesForm,
            ),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES,
                {"is_exceptional_circumstances": True},
                ExplainExceptionalCircumstancesForm,
            ),
        ),
    )
    def test_POST_to_step_success(
        self,
        step,
        data,
        expected_next_form,
        post_to_step,
        goto_step,
        mock_f680_application_get,
        force_has_made_previous_application,
    ):
        goto_step(step)
        response = post_to_step(
            step,
            data,
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], expected_next_form)

    @pytest.mark.parametrize(
        "step, data, expected_errors",
        (
            (FormSteps.APPLICATION_NAME, {"name": ""}, {"name": ["This field is required."]}),
            (FormSteps.EXCEPTIONAL_CIRCUMSTANCES, {}, {"is_exceptional_circumstances": ["This field is required."]}),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS,
                {},
                {
                    "exceptional_circumstances_date": ["Enter the day, month and year"],
                    "exceptional_circumstances_reason": ["This field is required."],
                },
            ),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS,
                {
                    "exceptional_circumstances_reason": "because",
                    "exceptional_circumstances_date_0": DATETIME_10_DAYS_AGO.day,
                    "exceptional_circumstances_date_1": DATETIME_10_DAYS_AGO.month,
                    "exceptional_circumstances_date_2": DATETIME_10_DAYS_AGO.year,
                },
                {
                    "exceptional_circumstances_date": ["Date must be in the future"],
                },
            ),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS,
                {
                    "exceptional_circumstances_reason": "because",
                    "exceptional_circumstances_date_0": DATETIME_IN_1_YEAR.day,
                    "exceptional_circumstances_date_1": DATETIME_IN_1_YEAR.month,
                    "exceptional_circumstances_date_2": DATETIME_IN_1_YEAR.year,
                },
                {
                    "exceptional_circumstances_date": ["Date must be within 30 days"],
                },
            ),
        ),
    )
    def test_POST_to_step_validation_error(
        self,
        step,
        data,
        expected_errors,
        post_to_step,
        goto_step,
        mock_f680_application_get,
        force_exceptional_circumstances,
    ):
        goto_step(step)
        response = post_to_step(
            step,
            data,
        )
        assert response.status_code == 200
        for field_name, error in expected_errors.items():
            assert response.context["form"][field_name].errors == error

    @freeze_time("2026-11-30")
    def test_POST_submit_wizard_success(
        self, post_to_step, goto_step, mock_f680_application_get, mock_patch_f680_application
    ):
        response = post_to_step(
            FormSteps.APPLICATION_NAME,
            {"name": "some test app"},
        )
        response = post_to_step(
            FormSteps.HAS_MADE_PREVIOUS_APPLICATION,
            {"has_made_previous_application": True},
        )
        response = post_to_step(
            FormSteps.PREVIOUS_APPLICATION,
            {"previous_application_ecju_reference": "123456", "previous_application_details": "some info"},
        )
        response = post_to_step(
            FormSteps.EXCEPTIONAL_CIRCUMSTANCES,
            {"is_exceptional_circumstances": True},
        )
        response = post_to_step(
            FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS,
            {
                "exceptional_circumstances_reason": "because",
                "exceptional_circumstances_date_0": "1",
                "exceptional_circumstances_date_1": "12",
                "exceptional_circumstances_date_2": "2026",
            },
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "general_application_details": {
                        "label": "General application details",
                        "fields": {
                            "name": {
                                "key": "name",
                                "answer": "some test app",
                                "raw_answer": "some test app",
                                "question": "Name the application",
                                "datatype": "string",
                            },
                            "has_made_previous_application": {
                                "key": "has_made_previous_application",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Have you made a previous application?",
                                "datatype": "boolean",
                            },
                            "previous_application_ecju_reference": {
                                "key": "previous_application_ecju_reference",
                                "answer": "123456",
                                "raw_answer": "123456",
                                "question": "What is the ECJU reference number?",
                                "datatype": "string",
                            },
                            "previous_application_details": {
                                "key": "previous_application_details",
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Can you provide more detail?",
                                "datatype": "string",
                            },
                            "is_exceptional_circumstances": {
                                "key": "is_exceptional_circumstances",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?",
                                "datatype": "boolean",
                            },
                            "exceptional_circumstances_date": {
                                "key": "exceptional_circumstances_date",
                                "answer": "2026-12-01",
                                "raw_answer": "2026-12-01",
                                "question": "When do you need your F680 approval?",
                                "datatype": "date",
                            },
                            "exceptional_circumstances_reason": {
                                "key": "exceptional_circumstances_reason",
                                "answer": "because",
                                "raw_answer": "because",
                                "question": "Why do you need approval in less than 30 days?",
                                "datatype": "string",
                            },
                        },
                        "type": "single",
                        "fields_sequence": [
                            "name",
                            "has_made_previous_application",
                            "previous_application_ecju_reference",
                            "previous_application_details",
                            "is_exceptional_circumstances",
                            "exceptional_circumstances_date",
                            "exceptional_circumstances_reason",
                        ],
                    },
                },
            }
        }

    @pytest.mark.parametrize(
        "step, expected_form, expected_initial",
        (
            (FormSteps.APPLICATION_NAME, ApplicationNameForm, {"name": "my first F680"}),
            (
                FormSteps.PREVIOUS_APPLICATION,
                PreviousApplicationsForm,
                {"previous_application_ecju_reference": "123456", "previous_application_details": "some info"},
            ),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES,
                ExceptionalCircumstancesForm,
                {"is_exceptional_circumstances": True},
            ),
            (
                FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS,
                ExplainExceptionalCircumstancesForm,
                {
                    "exceptional_circumstances_date": datetime.fromisoformat("2090-01-01"),
                    "exceptional_circumstances_reason": "some reason",
                },
            ),
        ),
    )
    def test_GET_with_existing_data_success(
        self,
        step,
        expected_form,
        expected_initial,
        authorized_client,
        mock_f680_application_get_existing_data,
        f680_application_wizard_url,
        goto_step,
        force_exceptional_circumstances,
        force_has_made_previous_application,
    ):
        response = goto_step(step)
        assert response.status_code == 200
        assert isinstance(response.context["form"], expected_form)
        for key, expected_value in expected_initial.items():
            assert response.context["form"][key].initial == expected_value
