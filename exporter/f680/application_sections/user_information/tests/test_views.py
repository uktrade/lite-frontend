import pytest

from django.urls import reverse
from freezegun import freeze_time

from core import client

from exporter.f680.application_sections.user_information import forms
from exporter.f680.application_sections.user_information.constants import FormSteps


@pytest.fixture(autouse=True)
def setup_tests(mock_countries):
    pass


@pytest.fixture
def missing_f680_application_wizard_url(missing_application_id):
    return reverse(
        "f680:user_information:wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_user_information_wizard_url(data_f680_case):
    return reverse(
        "f680:user_information:wizard",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def f680_edit_user_information_wizard_url(data_f680_case, data_item_id):
    return reverse(
        "f680:user_information:wizard",
        kwargs={"pk": data_f680_case["id"], "id": data_item_id},
    )


@pytest.fixture
def force_third_party(goto_step, post_to_step):
    goto_step(FormSteps.ENTITY_TYPE)
    post_to_step(
        FormSteps.ENTITY_TYPE,
        {"entity_type": "third_party"},
    )


@pytest.fixture
def data_item_id():
    return "d7b483ff-5d70-415f-a040-5866d6a7cb1b"  # /PS-IGNORE


@pytest.fixture
def mock_f680_application_get_existing_data(requests_mock, data_f680_case, data_item_id):
    data_f680_case["application"] = {
        "name": "vfd",
        "sections": {
            "user_information": {
                "items": [
                    {
                        "fields": {
                            "entity_type": {
                                "answer": "End user",
                                "datatype": "string",
                                "key": "entity_type",
                                "question": "Select type of entity",
                                "raw_answer": "end-user",
                            },
                            "end_user_name": {
                                "answer": "some end user name",
                                "datatype": "string",
                                "key": "end_user_name",
                                "question": "End-user name",
                                "raw_answer": "some end user name",
                            },
                            "address": {
                                "answer": "some address",
                                "datatype": "string",
                                "key": "address",
                                "question": "Address",
                                "raw_answer": "some address",
                            },
                            "country": {
                                "answer": "United States",
                                "datatype": "string",
                                "key": "country",
                                "question": "Country",
                                "raw_answer": "US",
                            },
                            "prefix": {
                                "answer": "some prefix",
                                "datatype": "string",
                                "key": "prefix",
                                "question": "Enter a prefix (optional)",
                                "raw_answer": "some prefix",
                            },
                            "security_classification": {
                                "answer": "Official",
                                "datatype": "string",
                                "key": "security_classification",
                                "question": "Select security classification",
                                "raw_answer": "official",
                            },
                            "suffix": {
                                "answer": "some suffix",
                                "datatype": "string",
                                "key": "suffix",
                                "question": "Enter a suffix (optional)",
                                "raw_answer": "some suffix",
                            },
                            "end_user_intended_end_use": {
                                "answer": "some end use",
                                "datatype": "string",
                                "key": "end_user_intended_end_use",
                                "question": "How does the end-user intend to use this item",
                                "raw_answer": "some end use",
                            },
                        },
                        "fields_sequence": [
                            "entity_type",
                            "end_user_name",
                            "address",
                            "country",
                            "prefix",
                            "security_classification",
                            "suffix",
                            "end_user_intended_end_use",
                        ],
                        "id": data_item_id,
                    }
                ],
                "label": "User Information",
                "type": "multiple",
            }
        },
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def post_to_step(post_to_step_factory, f680_user_information_wizard_url):
    return post_to_step_factory(f680_user_information_wizard_url)


@pytest.fixture
def goto_step(goto_step_factory, f680_user_information_wizard_url):
    return goto_step_factory(f680_user_information_wizard_url)


@pytest.fixture
def goto_edit_step(goto_step_factory, f680_edit_user_information_wizard_url):
    return goto_step_factory(f680_edit_user_information_wizard_url)


class TestUserInformationView:

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
        f680_user_information_wizard_url,
        data_f680_case,
    ):
        response = authorized_client.get(f680_user_information_wizard_url)
        assert response.status_code == 200
        assert response.context["back_link_url"] == reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})
        assert isinstance(response.context["form"], forms.EntityTypeForm)

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_user_information_wizard_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_user_information_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    @pytest.mark.parametrize(
        "step, data, expected_next_form",
        (
            (FormSteps.ENTITY_TYPE, {"entity_type": "end-user"}, forms.EndUserNameForm),
            (
                FormSteps.END_USER_NAME,
                {"end_user_name": "some end user name"},
                forms.EndUserAddressForm,
            ),
            (
                FormSteps.END_USER_ADDRESS,
                {"address": "some end user address", "country": "US"},
                forms.SecurityGradingForm,
            ),
            (
                FormSteps.SECURITY_GRADING,
                {
                    "prefix": "some prefix",
                    "security_classification": "official",
                    "suffix": "some suffix",
                },
                forms.EndUserIntendedEndUseForm,
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
            (FormSteps.ENTITY_TYPE, {"entity_type": ""}, {"entity_type": ["Select the type of entity"]}),
            (
                FormSteps.THIRD_PARTY_ROLE,
                {},
                {"third_party_role": ["Select a role"]},
            ),
            (
                FormSteps.END_USER_NAME,
                {},
                {"end_user_name": ["Enter a name"]},
            ),
            (
                FormSteps.END_USER_ADDRESS,
                {},
                {"address": ["Enter an address"], "country": ["Enter or select a country"]},
            ),
            (
                FormSteps.SECURITY_GRADING,
                {},
                {"security_classification": ["Select a security classification"]},
            ),
            (
                FormSteps.INTENDED_END_USE,
                {},
                {"end_user_intended_end_use": ["Enter how the end-user will use the item"]},
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
        force_third_party,
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
            FormSteps.ENTITY_TYPE,
            {"entity_type": "third-party"},
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.ThirdPartyRoleForm

        response = post_to_step(
            FormSteps.THIRD_PARTY_ROLE,
            {"third_party_role": "consultant"},
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserNameForm

        response = post_to_step(
            FormSteps.END_USER_NAME,
            {
                "end_user_name": "some end user name",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserAddressForm

        response = post_to_step(
            FormSteps.END_USER_ADDRESS,
            {
                "address": "some end user address",
                "country": "US",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.SecurityGradingForm

        response = post_to_step(
            FormSteps.SECURITY_GRADING,
            {
                "prefix": "some prefix",
                "security_classification": "secret",
                "suffix": "some suffix",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserIntendedEndUseForm

        response = post_to_step(
            FormSteps.INTENDED_END_USE,
            {
                "end_user_intended_end_use": "some end use",
            },
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        generated_uuid = mock_patch_f680_application.last_request.json()["application"]["sections"]["user_information"][
            "items"
        ][0]["id"]
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "user_information": {
                        "label": "User Information",
                        "items": [
                            {
                                "id": generated_uuid,
                                "fields": {
                                    "entity_type": {
                                        "key": "entity_type",
                                        "answer": "Third party",
                                        "raw_answer": "third-party",
                                        "question": "Select type of entity",
                                        "datatype": "string",
                                    },
                                    "third_party_role": {
                                        "key": "third_party_role",
                                        "answer": "Consultant",
                                        "raw_answer": "consultant",
                                        "question": "Select the role of the third party",
                                        "datatype": "string",
                                    },
                                    "end_user_name": {
                                        "key": "end_user_name",
                                        "answer": "some end user name",
                                        "raw_answer": "some end user name",
                                        "question": "End-user name",
                                        "datatype": "string",
                                    },
                                    "address": {
                                        "key": "address",
                                        "answer": "some end user address",
                                        "raw_answer": "some end user address",
                                        "question": "Address",
                                        "datatype": "string",
                                    },
                                    "country": {
                                        "key": "country",
                                        "answer": "United States",
                                        "raw_answer": "US",
                                        "question": "Country",
                                        "datatype": "string",
                                    },
                                    "prefix": {
                                        "key": "prefix",
                                        "answer": "some prefix",
                                        "raw_answer": "some prefix",
                                        "question": "Enter a prefix (optional)",
                                        "datatype": "string",
                                    },
                                    "security_classification": {
                                        "key": "security_classification",
                                        "answer": "Secret",
                                        "raw_answer": "secret",
                                        "question": "Select security classification",
                                        "datatype": "string",
                                    },
                                    "other_security_classification": {
                                        "key": "other_security_classification",
                                        "answer": "",
                                        "raw_answer": "",
                                        "question": "Enter the security classification",
                                        "datatype": "string",
                                    },
                                    "suffix": {
                                        "key": "suffix",
                                        "answer": "some suffix",
                                        "raw_answer": "some suffix",
                                        "question": "Enter a suffix (optional)",
                                        "datatype": "string",
                                    },
                                    "end_user_intended_end_use": {
                                        "key": "end_user_intended_end_use",
                                        "answer": "some end use",
                                        "raw_answer": "some end use",
                                        "question": "How does the end-user intend to use this item",
                                        "datatype": "string",
                                    },
                                },
                                "fields_sequence": [
                                    "entity_type",
                                    "third_party_role",
                                    "end_user_name",
                                    "address",
                                    "country",
                                    "prefix",
                                    "security_classification",
                                    "other_security_classification",
                                    "suffix",
                                    "end_user_intended_end_use",
                                ],
                            }
                        ],
                        "type": "multiple",
                    }
                },
            }
        }

    @freeze_time("2026-11-30")
    def test_POST_submit_wizard_existing_user_information_success(
        self,
        post_to_step,
        goto_step,
        mock_f680_application_get_existing_data,
        mock_patch_f680_application,
        data_item_id,
    ):
        response = post_to_step(
            FormSteps.ENTITY_TYPE,
            {"entity_type": "third-party"},
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.ThirdPartyRoleForm

        response = post_to_step(
            FormSteps.THIRD_PARTY_ROLE,
            {"third_party_role": "consultant"},
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserNameForm

        response = post_to_step(
            FormSteps.END_USER_NAME,
            {
                "end_user_name": "some end user name",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserAddressForm

        response = post_to_step(
            FormSteps.END_USER_ADDRESS,
            {
                "address": "some end user address",
                "country": "US",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.SecurityGradingForm

        response = post_to_step(
            FormSteps.SECURITY_GRADING,
            {
                "prefix": "some prefix",
                "security_classification": "secret",
                "suffix": "some suffix",
            },
        )
        assert response.status_code == 200
        assert type(response.context["form"]) == forms.EndUserIntendedEndUseForm

        response = post_to_step(
            FormSteps.INTENDED_END_USE,
            {
                "end_user_intended_end_use": "some end use",
            },
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        api_patch_payload = mock_patch_f680_application.last_request.json()
        generated_uuid = mock_patch_f680_application.last_request.json()["application"]["sections"]["user_information"][
            "items"
        ][1]["id"]
        # existing record still present
        assert api_patch_payload["application"]["sections"]["user_information"]["items"][0]["id"] == data_item_id

        # New record also present
        assert api_patch_payload["application"]["sections"]["user_information"]["items"][1] == {
            "id": generated_uuid,
            "fields": {
                "entity_type": {
                    "key": "entity_type",
                    "answer": "Third party",
                    "raw_answer": "third-party",
                    "question": "Select type of entity",
                    "datatype": "string",
                },
                "third_party_role": {
                    "key": "third_party_role",
                    "answer": "Consultant",
                    "raw_answer": "consultant",
                    "question": "Select the role of the third party",
                    "datatype": "string",
                },
                "end_user_name": {
                    "key": "end_user_name",
                    "answer": "some end user name",
                    "raw_answer": "some end user name",
                    "question": "End-user name",
                    "datatype": "string",
                },
                "address": {
                    "key": "address",
                    "answer": "some end user address",
                    "raw_answer": "some end user address",
                    "question": "Address",
                    "datatype": "string",
                },
                "country": {
                    "key": "country",
                    "answer": "United States",
                    "raw_answer": "US",
                    "question": "Country",
                    "datatype": "string",
                },
                "prefix": {
                    "key": "prefix",
                    "answer": "some prefix",
                    "raw_answer": "some prefix",
                    "question": "Enter a prefix (optional)",
                    "datatype": "string",
                },
                "security_classification": {
                    "key": "security_classification",
                    "answer": "Secret",
                    "raw_answer": "secret",
                    "question": "Select security classification",
                    "datatype": "string",
                },
                "other_security_classification": {
                    "key": "other_security_classification",
                    "answer": "",
                    "raw_answer": "",
                    "question": "Enter the security classification",
                    "datatype": "string",
                },
                "suffix": {
                    "key": "suffix",
                    "answer": "some suffix",
                    "raw_answer": "some suffix",
                    "question": "Enter a suffix (optional)",
                    "datatype": "string",
                },
                "end_user_intended_end_use": {
                    "key": "end_user_intended_end_use",
                    "answer": "some end use",
                    "raw_answer": "some end use",
                    "question": "How does the end-user intend to use this item",
                    "datatype": "string",
                },
            },
            "fields_sequence": [
                "entity_type",
                "third_party_role",
                "end_user_name",
                "address",
                "country",
                "prefix",
                "security_classification",
                "other_security_classification",
                "suffix",
                "end_user_intended_end_use",
            ],
        }

    @pytest.mark.parametrize(
        "step, expected_form, expected_initial",
        (
            (FormSteps.ENTITY_TYPE, forms.EntityTypeForm, {"entity_type": "end-user"}),
            (
                FormSteps.END_USER_NAME,
                forms.EndUserNameForm,
                {"end_user_name": "some end user name"},
            ),
            (
                FormSteps.END_USER_ADDRESS,
                forms.EndUserAddressForm,
                {"address": "some address", "country": "US"},
            ),
            (
                FormSteps.SECURITY_GRADING,
                forms.SecurityGradingForm,
                {
                    "prefix": "some prefix",
                    "security_classification": "official",
                    "suffix": "some suffix",
                },
            ),
            (
                FormSteps.INTENDED_END_USE,
                forms.EndUserIntendedEndUseForm,
                {"end_user_intended_end_use": "some end use"},
            ),
        ),
    )
    def test_GET_with_existing_data_success(
        self,
        step,
        expected_form,
        expected_initial,
        mock_f680_application_get_existing_data,
        goto_edit_step,
    ):
        response = goto_edit_step(step)
        assert response.status_code == 200
        assert isinstance(response.context["form"], expected_form)
        for key, expected_value in expected_initial.items():
            assert response.context["form"][key].initial == expected_value


@pytest.fixture
def f680_user_information_summary_url(data_f680_case):
    return reverse(
        "f680:user_information:summary",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def missing_f680_user_information_summary_url(missing_application_id):
    return reverse(
        "f680:user_information:summary",
        kwargs={"pk": missing_application_id},
    )


class TestUserInformationSummaryView:

    def test_GET_with_existing_data_success(
        self,
        authorized_client,
        f680_user_information_summary_url,
        mock_f680_application_get_existing_data,
        data_item_id,
    ):
        response = authorized_client.get(f680_user_information_summary_url)
        assert response.status_code == 200
        assert response.context["user_entities"] == {
            data_item_id: {
                "entity_type": "End user",
                "end_user_name": "some end user name",
                "address": "some address",
                "country": "United States",
                "prefix": "some prefix",
                "security_classification": "Official",
                "suffix": "some suffix",
                "end_user_intended_end_use": "some end use",
            }
        }

    def test_GET_no_application_404(
        self,
        authorized_client,
        missing_f680_user_information_summary_url,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(missing_f680_application_wizard_url)
        assert response.status_code == 404

    def test_GET_no_user_entities_redirects(
        self,
        authorized_client,
        f680_user_information_summary_url,
        mock_f680_application_get,
    ):
        response = authorized_client.get(f680_user_information_summary_url)
        assert response.status_code == 302

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_user_information_summary_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_user_information_summary_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    @pytest.mark.parametrize(
        "step, data, required_field, expected_errors",
        (
            (
                FormSteps.SECURITY_GRADING,
                {"security_classification": "other", "other_security_classification": ""},
                "other_security_classification",
                ["Security classification cannot be blank"],
            ),
        ),
    )
    def test_POST_to_step_with_required_conditional_validation_error(
        self,
        step,
        data,
        required_field,
        expected_errors,
        post_to_step,
        goto_step,
        mock_f680_application_get,
        force_third_party,
    ):
        goto_step(step)
        response = post_to_step(
            step,
            data,
        )
        assert response.status_code == 200
        assert response.context["form"][required_field].errors == expected_errors
