import pytest
from datetime import datetime

from django.urls import reverse

from core import client

from .. import forms
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
def missing_f680_approval_type_wizard_url(missing_application_id):
    return reverse(
        "f680:approval_details:type_wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_approval_type_wizard_url(data_f680_case):
    return reverse(
        "f680:approval_details:type_wizard",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def missing_f680_product_wizard_url(missing_application_id):
    return reverse(
        "f680:approval_details:product_wizard",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_product_wizard_url(data_f680_case):
    return reverse(
        "f680:approval_details:product_wizard",
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
def mock_patch_f680_application(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.patch(url=url, json=data_f680_case)


@pytest.fixture
def post_to_approval_type_step(post_to_step_factory, f680_approval_type_wizard_url):
    return post_to_step_factory(f680_approval_type_wizard_url)


@pytest.fixture
def goto_approval_type_step(goto_step_factory, f680_approval_type_wizard_url):
    return goto_step_factory(f680_approval_type_wizard_url)


@pytest.fixture
def post_to_product_step(post_to_step_factory, f680_product_wizard_url):
    return post_to_step_factory(f680_product_wizard_url)


@pytest.fixture
def goto_product_step(goto_step_factory, f680_product_wizard_url):
    return goto_step_factory(f680_product_wizard_url)


@pytest.fixture
def force_foreign_tech(goto_product_step, post_to_product_step):
    goto_product_step(FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED)
    post_to_product_step(
        FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
        {"is_foreign_tech_or_information_shared": True},
    )


@pytest.fixture
def force_product_under_itar(goto_product_step, post_to_product_step):
    goto_product_step(FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR)
    post_to_product_step(
        FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
        {"is_controlled_under_itar": True, "controlled_info": "some info"},
    )


@pytest.fixture
def force_has_security_classification(goto_product_step, post_to_product_step):
    goto_product_step(FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION)
    post_to_product_step(
        FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
        {"has_security_classification": True},
    )


@pytest.fixture
def force_is_not_security_classified(goto_product_step, post_to_product_step):
    goto_product_step(FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION)
    post_to_product_step(
        FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
        {"has_security_classification": False},
    )


@pytest.fixture
def force_mod_funded(goto_product_step, post_to_product_step):
    goto_product_step(FormSteps.PRODUCT_FUNDING)
    post_to_product_step(
        FormSteps.PRODUCT_FUNDING,
        {"funding_source": "mod"},
    )


class TestApprovalDetailsView:

    def test_GET_no_application_404(
        self,
        authorized_client,
        missing_f680_approval_type_wizard_url,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(missing_f680_approval_type_wizard_url)
        assert response.status_code == 404

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_approval_type_wizard_url,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ApprovalTypeForm)

    def test_GET_success_with_organisation_set(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_approval_type_wizard_url,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ApprovalTypeForm)

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_approval_type_wizard_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_GET_no_feature_organisation_allowed(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_approval_type_wizard_url,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_POST_approval_type_and_submit_wizard_success(
        self,
        post_to_approval_type_step,
        goto_approval_type_step,
        mock_f680_application_get,
        mock_patch_f680_application,
    ):
        response = post_to_approval_type_step(
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

    def test_POST_to_approval_type_validation_error(
        self,
        post_to_approval_type_step,
        goto_approval_type_step,
        mock_f680_application_get,
    ):
        goto_approval_type_step(FormSteps.APPROVAL_TYPE)
        response = post_to_approval_type_step(
            FormSteps.APPROVAL_TYPE,
            {},
        )
        assert response.status_code == 200
        assert "Select an approval choice" in response.context["form"]["approval_choices"].errors

    def test_GET_with_existing_data_success(
        self,
        authorized_client,
        mock_f680_application_get_existing_data,
        f680_approval_type_wizard_url,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ApprovalTypeForm)
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


class TestProductInformationViews:

    def test_GET_no_application_404(
        self,
        authorized_client,
        missing_f680_product_wizard_url,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(missing_f680_product_wizard_url)
        assert response.status_code == 404

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_product_wizard_url,
    ):
        response = authorized_client.get(f680_product_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ProductNameForm)

    def test_GET_success_with_organisation_set(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_product_wizard_url,
        set_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_product_wizard_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ProductNameForm)

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_product_wizard_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_product_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_GET_no_feature_organisation_allowed(
        self,
        authorized_client,
        mock_f680_application_get,
        f680_product_wizard_url,
        unset_f680_allowed_organisation,
    ):
        response = authorized_client.get(f680_product_wizard_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    @pytest.mark.parametrize(
        "step, data, expected_next_form",
        (
            (FormSteps.PRODUCT_NAME, {"product_name": "Test Name"}, forms.ProductDescription),
            (
                FormSteps.PRODUCT_DESCRIPTION,
                {"product_description": "Does a thing"},
                forms.ProductHasSecurityClassification,
            ),
            (
                FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
                {"has_security_classification": True},
                forms.ProductSecurityClassificationForm,
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "prefix": "some prefix",
                    "security_classification": "unclassified",
                    "suffix": "some suffix",
                    "issuing_authority_name_address": "some address",
                    "reference": "some ref",
                    "date_of_issue_0": "1",
                    "date_of_issue_1": "1",
                    "date_of_issue_2": "2024",
                },
                forms.ProductForeignTechOrSharedInformation,
            ),
            (
                FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
                {"is_foreign_tech_or_information_shared": True},
                forms.ProductControlledUnderItar,
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {"is_controlled_under_itar": True, "controlled_info": "some info"},
                forms.ProductControlledUnderItarDetails,
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS,
                {
                    "controlled_information": "secret stuff",
                    "itar_reference_number": "123456",
                    "usml_categories": "none",
                    "itar_approval_scope": "no scope",
                    "expected_time_in_possession": "10 years",
                },
                forms.ProductIncludeCryptography,
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {
                    "is_including_cryptography_or_security_features": True,
                    "cryptography_or_security_feature_info": "some info",
                },
                forms.ProductRatedUnderMTCR,
            ),
            (
                FormSteps.PRODUCT_RATED_UNDER_MTCR,
                {"is_item_rated_under_mctr": "mtcr_1"},
                forms.ProductMANPADs,
            ),
            (
                FormSteps.PRODUCT_MANPAD,
                {"is_item_manpad": "no"},
                forms.ProductElectronicMODData,
            ),
            (
                FormSteps.PRODUCT_ELECTRONICMODDATA,
                {"is_mod_electronic_data_shared": "no"},
                forms.ProductFunding,
            ),
            (
                FormSteps.PRODUCT_FUNDING,
                {"funding_source": "private_venture"},
                forms.ProductUsedByUKArmedForces,
            ),
        ),
    )
    def test_POST_to_step_success(
        self,
        step,
        data,
        expected_next_form,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_has_security_classification,
        force_foreign_tech,
        force_product_under_itar,
    ):
        goto_product_step(step)
        response = post_to_product_step(
            step,
            data,
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], expected_next_form)

    @pytest.mark.parametrize(
        "step, data, expected_errors",
        (
            (FormSteps.PRODUCT_NAME, {"product_name": ""}, {"product_name": ["This field is required."]}),
            (
                FormSteps.PRODUCT_DESCRIPTION,
                {"product_description": ""},
                {"product_description": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
                {},
                {"has_security_classification": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                },
                {
                    "issuing_authority_name_address": ["This field is required."],
                    "reference": ["This field is required."],
                    "date_of_issue": ["Enter the date of issue"],
                },
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                    "issuing_authority_name_address": "some address",
                    "reference": "some reference",
                    "date_of_issue_0": "20",
                },
                {
                    "date_of_issue": ["Date of issue must include a month", "Date of issue must include a year"],
                },
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                    "issuing_authority_name_address": "some address",
                    "reference": "some reference",
                    "date_of_issue_0": "20",
                    "date_of_issue_2": "2020",
                },
                {
                    "date_of_issue": ["Date of issue must include a month"],
                },
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                    "issuing_authority_name_address": "some address",
                    "reference": "some reference",
                    "date_of_issue_0": "20",
                    "date_of_issue_1": "2",
                    "date_of_issue_2": "2040",
                },
                {
                    "date_of_issue": ["Date of issue must be in the past"],
                },
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                    "issuing_authority_name_address": "some address",
                    "reference": "some reference",
                    "date_of_issue_0": "50",
                    "date_of_issue_1": "2",
                    "date_of_issue_2": "2020",
                },
                {
                    "date_of_issue": ["Date of issue must be a real date"],
                },
            ),
            (
                FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
                {},
                {"is_foreign_tech_or_information_shared": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {},
                {"is_including_cryptography_or_security_features": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_RATED_UNDER_MTCR,
                {"is_item_rated_under_mctr": ""},
                {"is_item_rated_under_mctr": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_MANPAD,
                {"is_item_manpad": ""},
                {"is_item_manpad": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_ELECTRONICMODDATA,
                {"is_mod_electronic_data_shared": ""},
                {"is_mod_electronic_data_shared": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_FUNDING,
                {"funding_source": ""},
                {"funding_source": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {},
                {"is_controlled_under_itar": ["This field is required."]},
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS,
                {
                    "controlled_information": "",
                    "itar_reference_number": "",
                    "usml_categories": "",
                    "itar_approval_scope": "",
                    "expected_time_in_possession": "",
                },
                {
                    "controlled_information": ["This field is required."],
                    "itar_reference_number": ["This field is required."],
                    "usml_categories": ["This field is required."],
                    "itar_approval_scope": ["This field is required."],
                    "expected_time_in_possession": ["This field is required."],
                },
            ),
        ),
    )
    def test_POST_to_step_validation_error(
        self,
        step,
        data,
        expected_errors,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_has_security_classification,
        force_foreign_tech,
        force_product_under_itar,
    ):
        goto_product_step(step)
        response = post_to_product_step(
            step,
            data,
        )
        assert response.status_code == 200
        for field_name, error in expected_errors.items():
            assert response.context["form"][field_name].errors == error

    def test_POST_to_step_actions_to_classify_validation_error(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_foreign_tech,
        force_product_under_itar,
        force_is_not_security_classified,
    ):
        goto_product_step(FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT)
        response = post_to_product_step(
            FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT,
            {"actions_to_classify": ""},
        )
        assert response.status_code == 200
        response.context["form"]["actions_to_classify"].errors == ["This field is required."]

    def test_POST_submit_wizard_success(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        mock_patch_f680_application,
        force_has_security_classification,
        force_foreign_tech,
        force_product_under_itar,
        force_mod_funded,
    ):
        response = post_to_product_step(
            FormSteps.PRODUCT_NAME,
            {"product_name": "Test Name"},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_DESCRIPTION,
            {"product_description": "Does a thing"},
        )
        response = (
            post_to_product_step(
                FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
                {"has_security_classification": True},
            ),
        )
        response = (
            post_to_product_step(
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "prefix": "some prefix",
                    "security_classification": "unclassified",
                    "suffix": "some suffix",
                    "issuing_authority_name_address": "some address",
                    "reference": "1234",
                    "date_of_issue_0": "1",
                    "date_of_issue_1": "1",
                    "date_of_issue_2": "2025",
                },
            ),
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
            {"is_foreign_tech_or_information_shared": True},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
            {"is_controlled_under_itar": True, "controlled_info": "some info"},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS,
            {
                "controlled_information": "secret stuff",
                "itar_reference_number": "123456",
                "usml_categories": "none",
                "itar_approval_scope": "no scope",
                "expected_time_in_possession": "10 years",
            },
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
            {
                "is_including_cryptography_or_security_features": True,
                "cryptography_or_security_feature_info": "some info",
            },
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_RATED_UNDER_MTCR,
            {"is_item_rated_under_mctr": "mtcr_1"},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_MANPAD,
            {"is_item_manpad": "no"},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_ELECTRONICMODDATA,
            {"is_mod_electronic_data_shared": "no"},
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_FUNDING,
            {"funding_source": "mod"},
        )
        response = post_to_product_step(
            FormSteps.MOD_SPONSOR_DETAILS,
            {
                "full_name": "a name",
                "address": "16 Street",
                "phone_number": "01234785785",
                "email_address": "test@test.com",
            },
        )
        response = post_to_product_step(
            FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES,
            {"is_used_by_uk_armed_forces": True, "used_by_uk_armed_forces_info": "some info"},
        )

        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "product_information": {
                        "label": "Product information",
                        "fields": [
                            {
                                "key": "product_name",
                                "answer": "Test Name",
                                "raw_answer": "Test Name",
                                "question": "Give the item a descriptive name",
                                "datatype": "string",
                            },
                            {
                                "key": "product_description",
                                "answer": "Does a thing",
                                "raw_answer": "Does a thing",
                                "question": "Describe the item",
                                "datatype": "string",
                            },
                            {
                                "key": "has_security_classification",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Has the product been given a security classifcation by a UK MOD authority?",
                                "datatype": "boolean",
                            },
                            {
                                "key": "prefix",
                                "answer": "some prefix",
                                "raw_answer": "some prefix",
                                "question": "Enter a prefix (optional)",
                                "datatype": "string",
                            },
                            {
                                "key": "security_classification",
                                "answer": "Unclassified",
                                "raw_answer": "unclassified",
                                "question": "Select security classification",
                                "datatype": "string",
                            },
                            {
                                "key": "other_security_classification",
                                "answer": "",
                                "raw_answer": "",
                                "question": "Enter the security classification",
                                "datatype": "string",
                            },
                            {
                                "key": "suffix",
                                "answer": "some suffix",
                                "raw_answer": "some suffix",
                                "question": "Enter a suffix (optional)",
                                "datatype": "string",
                            },
                            {
                                "key": "issuing_authority_name_address",
                                "answer": "some address",
                                "raw_answer": "some address",
                                "question": "Name and address of the issuing authority",
                                "datatype": "string",
                            },
                            {
                                "key": "reference",
                                "answer": "1234",
                                "raw_answer": "1234",
                                "question": "Reference",
                                "datatype": "string",
                            },
                            {
                                "key": "date_of_issue",
                                "answer": "2025-01-01",
                                "raw_answer": "2025-01-01",
                                "question": "Date of issue",
                                "datatype": "date",
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
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Explain how the technology or information is controlled.Include countries classification levels and reference numbers.  You can upload supporting documents later in your application",
                                "datatype": "string",
                            },
                            {
                                "key": "controlled_information",
                                "answer": "secret stuff",
                                "raw_answer": "secret stuff",
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
                                "answer": "none",
                                "raw_answer": "none",
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
                                "answer": "some info",
                                "raw_answer": "some info",
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
                                "key": "full_name",
                                "answer": "a name",
                                "raw_answer": "a name",
                                "question": "Full name",
                                "datatype": "string",
                            },
                            {
                                "key": "address",
                                "answer": "16 Street",
                                "raw_answer": "16 Street",
                                "question": "Address",
                                "datatype": "string",
                            },
                            {
                                "key": "phone_number",
                                "answer": "01234785785",
                                "raw_answer": "01234785785",
                                "question": "Phone number",
                                "datatype": "string",
                            },
                            {
                                "key": "email_address",
                                "answer": "test@test.com",
                                "raw_answer": "test@test.com",
                                "question": "Email address",
                                "datatype": "string",
                            },
                            {
                                "key": "is_used_by_uk_armed_forces",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Will the item be used by the UK Armed Forces?",
                                "datatype": "boolean",
                            },
                            {
                                "key": "used_by_uk_armed_forces_info",
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Explain how it will be used",
                                "datatype": "string",
                            },
                        ],
                        "type": "single",
                    }
                },
            }
        }

    @pytest.mark.parametrize(
        "step, expected_form, expected_initial",
        (
            (FormSteps.PRODUCT_NAME, forms.ProductNameForm, {"product_name": "Test Info"}),
            (
                FormSteps.PRODUCT_DESCRIPTION,
                forms.ProductDescription,
                {"product_description": "It does things"},
            ),
            (
                FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
                forms.ProductHasSecurityClassification,
                {"has_security_classification": True},
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                forms.ProductSecurityClassificationForm,
                {
                    "prefix": "some prefix",
                    "security_classification": "unclassified",
                    "suffix": "some suffix",
                    "issuing_authority_name_address": "Some address",
                    "reference": "1234",
                    "date_of_issue": datetime(year=2024, month=1, day=1),
                },
            ),
            (
                FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
                forms.ProductForeignTechOrSharedInformation,
                {"is_foreign_tech_or_information_shared": True},
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                forms.ProductControlledUnderItar,
                {"is_controlled_under_itar": True},
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS,
                forms.ProductControlledUnderItarDetails,
                {
                    "controlled_information": "Some info",
                    "itar_reference_number": "123456",
                    "usml_categories": "cat 1",
                    "itar_approval_scope": "no scope",
                    "expected_time_in_possession": "10 years",
                },
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                forms.ProductIncludeCryptography,
                {"is_including_cryptography_or_security_features": True},
            ),
            (
                FormSteps.PRODUCT_RATED_UNDER_MTCR,
                forms.ProductRatedUnderMTCR,
                {"is_item_rated_under_mctr": "mtcr_1"},
            ),
            (
                FormSteps.PRODUCT_MANPAD,
                forms.ProductMANPADs,
                {"is_item_manpad": "no"},
            ),
            (
                FormSteps.PRODUCT_ELECTRONICMODDATA,
                forms.ProductElectronicMODData,
                {"is_mod_electronic_data_shared": "no"},
            ),
            (
                FormSteps.PRODUCT_FUNDING,
                forms.ProductFunding,
                {"funding_source": "mod"},
            ),
            (
                FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES,
                forms.ProductUsedByUKArmedForces,
                {"is_used_by_uk_armed_forces": False},
            ),
        ),
    )
    def test_GET_with_existing_data_success(
        self,
        step,
        expected_form,
        post_to_product_step,
        goto_product_step,
        expected_initial,
        mock_f680_application_get_existing_data,
        force_has_security_classification,
        force_foreign_tech,
        force_product_under_itar,
    ):
        response = goto_product_step(step)
        assert response.status_code == 200
        assert isinstance(response.context["form"], expected_form)
        for key, expected_value in expected_initial.items():
            assert response.context["form"][key].initial == expected_value

    def test_GET_with_actions_to_classify_data_success(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get_existing_data,
        force_foreign_tech,
        force_product_under_itar,
        force_is_not_security_classified,
    ):
        response = goto_product_step(FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT)
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ActionTakenToClassifyInfo)
        response.context["form"]["actions_to_classify"].initial == "some actions"

    def test_POST_to_is_foreign_tech_or_information_shared_false_displays_correct_form(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
    ):

        goto_product_step(FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED)
        response = post_to_product_step(
            FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED,
            {"is_foreign_tech_or_information_shared": False},
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ProductIncludeCryptography)

    def test_POST_to_is_controlled_under_itar_false_displays_correct_form(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_foreign_tech,
    ):

        goto_product_step(FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR)
        response = post_to_product_step(
            FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
            {"is_controlled_under_itar": False, "controlled_info": "some info"},
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ProductIncludeCryptography)

    def test_POST_to_is_not_security_classified_displays_correct_form(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_is_not_security_classified,
    ):

        goto_product_step(FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION)
        response = post_to_product_step(
            FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
            {"has_security_classification": False},
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ActionTakenToClassifyInfo)

    def test_POST_to_actions_to_classify_displays_correct_form(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        force_is_not_security_classified,
    ):
        goto_product_step(FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT)
        response = post_to_product_step(
            FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT,
            {"actions_to_classify": "some actions"},
        )
        assert response.status_code == 200
        assert isinstance(response.context["form"], forms.ProductForeignTechOrSharedInformation)

    @pytest.mark.parametrize(
        "step, data, required_field",
        (
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {"is_controlled_under_itar": False, "controlled_info": ""},
                "controlled_info",
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {"is_including_cryptography_or_security_features": True, "cryptography_or_security_feature_info": ""},
                "cryptography_or_security_feature_info",
            ),
            (
                FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES,
                {"is_used_by_uk_armed_forces": True, "used_by_uk_armed_forces_info": ""},
                "used_by_uk_armed_forces_info",
            ),
        ),
    )
    def test_POST_to_step_with_required_conditional_validation_error(
        self,
        post_to_product_step,
        goto_product_step,
        mock_f680_application_get,
        step,
        data,
        required_field,
        force_has_security_classification,
        force_foreign_tech,
        force_product_under_itar,
    ):
        goto_product_step(step)
        response = post_to_product_step(
            step,
            data,
        )
        assert response.status_code == 200

        assert response.context["form"][required_field].errors == ["Required information"]
