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
        data_f680_case,
    ):
        response = authorized_client.get(f680_approval_type_wizard_url)
        assert response.status_code == 200
        assert response.context["back_link_url"] == reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})
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
            {
                "approval_choices": ["demonstration_in_uk", "demonstration_overseas", "training", "supply"],
                "approval_details_text": "some text",
                "demonstration_in_uk": "details",
                "demonstration_overseas": "details",
            },
        )
        assert response.status_code == 302
        assert mock_patch_f680_application.called_once
        assert mock_patch_f680_application.last_request.json() == {
            "application": {
                "name": "F680 Test 1",
                "sections": {
                    "approval_type": {
                        "label": "Approval type",
                        "fields": {
                            "approval_choices": {
                                "key": "approval_choices",
                                "answer": [
                                    "Demonstration in the United Kingdom to overseas customers",
                                    "Demonstration overseas",
                                    "Training",
                                    "Supply",
                                ],
                                "raw_answer": ["demonstration_in_uk", "demonstration_overseas", "training", "supply"],
                                "question": "Select the types of approvals you need",
                                "datatype": "list",
                            },
                            "demonstration_in_uk": {
                                "key": "demonstration_in_uk",
                                "answer": "details",
                                "raw_answer": "details",
                                "question": "Explain what you are demonstrating and why",
                                "datatype": "string",
                            },
                            "demonstration_overseas": {
                                "key": "demonstration_overseas",
                                "answer": "details",
                                "raw_answer": "details",
                                "question": "Explain what you are demonstrating and why",
                                "datatype": "string",
                            },
                            "approval_details_text": {
                                "key": "approval_details_text",
                                "answer": "some text",
                                "raw_answer": "some text",
                                "question": "Provide details about what you're seeking approval to do",
                                "datatype": "string",
                            },
                        },
                        "type": "single",
                        "fields_sequence": [
                            "approval_choices",
                            "demonstration_in_uk",
                            "demonstration_overseas",
                            "approval_details_text",
                        ],
                    }
                },
            }
        }

    @pytest.mark.parametrize(
        "data, expected_errors",
        (
            ({}, {"approval_choices": ["Select an approval choice"]}),
            (
                {"approval_choices": "demonstration_in_uk"},
                {"demonstration_in_uk": ["What you're demonstrating and why cannot be blank"]},
            ),
            (
                {"approval_choices": "demonstration_overseas"},
                {"demonstration_overseas": ["What you're demonstrating and why cannot be blank"]},
            ),
        ),
    )
    def test_POST_to_approval_type_validation_error(
        self,
        post_to_approval_type_step,
        goto_approval_type_step,
        mock_f680_application_get,
        data,
        expected_errors,
    ):
        goto_approval_type_step(FormSteps.APPROVAL_TYPE)
        response = post_to_approval_type_step(
            FormSteps.APPROVAL_TYPE,
            data,
        )
        assert response.status_code == 200

        for field_name, error in expected_errors.items():
            assert response.context["form"][field_name].errors == error

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
        data_f680_case,
    ):
        response = authorized_client.get(f680_product_wizard_url)
        assert response.status_code == 200
        assert response.context["back_link_url"] == reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})
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
            (FormSteps.PRODUCT_NAME, {"product_name": ""}, {"product_name": ["Enter a descriptive name"]}),
            (
                FormSteps.PRODUCT_DESCRIPTION,
                {"product_description": ""},
                {"product_description": ["Enter a description"]},
            ),
            (
                FormSteps.PRODUCT_HAS_SECURITY_CLASSIFICATION,
                {},
                {"has_security_classification": ["Select yes if you have a security classification"]},
            ),
            (
                FormSteps.ACTION_TAKEN_TO_CLASSIFY_PRODUCT,
                {},
                {"actions_to_classify": ["Enter details about what you have done to get the item security classified"]},
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "unclassified",
                },
                {
                    "issuing_authority_name_address": ["Enter who issued the security classification"],
                    "reference": ["Enter a reference"],
                    "date_of_issue": ["Enter the date of issue"],
                },
            ),
            (
                FormSteps.PRODUCT_SECURITY_CLASSIFICATION_DETAILS,
                {
                    "security_classification": "other",
                },
                {
                    "other_security_classification": ["Security classification cannot be blank"],
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
                {"is_foreign_tech_or_information_shared": ["Select yes if you will be sharing foreign technology"]},
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {},
                {
                    "is_including_cryptography_or_security_features": [
                        "Select yes if the item includes information security features"
                    ]
                },
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {"is_including_cryptography_or_security_features": True},
                {
                    "cryptography_or_security_feature_info": [
                        "Details about the information security features cannot be blank"
                    ]
                },
            ),
            (
                FormSteps.PRODUCT_RATED_UNDER_MTCR,
                {"is_item_rated_under_mctr": ""},
                {"is_item_rated_under_mctr": ["Select yes if the product is rated under MTCR"]},
            ),
            (
                FormSteps.PRODUCT_MANPAD,
                {"is_item_manpad": ""},
                {"is_item_manpad": ["Select yes if the product is a MANPADS"]},
            ),
            (
                FormSteps.PRODUCT_ELECTRONICMODDATA,
                {"is_mod_electronic_data_shared": ""},
                {"is_mod_electronic_data_shared": ["Select yes if EW data will be shared"]},
            ),
            (
                FormSteps.PRODUCT_FUNDING,
                {"funding_source": ""},
                {"funding_source": ["Select who is funding the item"]},
            ),
            (
                FormSteps.MOD_SPONSOR_DETAILS,
                {
                    "full_name": "",
                    "address": "",
                    "phone_number": "",
                    "email_address": "",
                },
                {
                    "full_name": ["Enter the sponsor's full name"],
                    "address": ["Enter the sponsor's address"],
                    "phone_number": ["Enter the sponsor's phone number"],
                    "email_address": ["Enter the sponsor's email address"],
                },
            ),
            (
                FormSteps.MOD_SPONSOR_DETAILS,
                {
                    "full_name": "John Bloggs",
                    "address": "62 Soapy Bubble Street",
                    "phone_number": "07777 123 123",
                    "email_address": "bork",
                },
                {
                    "email_address": ["Enter an email address in the correct format, like name@example.com"],
                },
            ),
            (
                FormSteps.MOD_SPONSOR_DETAILS,
                {
                    "full_name": "John Bloggs",
                    "address": "62 Soapy Bubble Street",
                    "phone_number": "bork",
                    "email_address": "test@email.com",
                },
                {
                    "phone_number": ["Enter a phone number, like 02890 960 001, 07787 900 982 or +447787 570 192"],
                },
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {},
                {"is_controlled_under_itar": ["Select yes if the foreign technology is controlled under ITAR"]},
            ),
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {
                    "is_controlled_under_itar": False,
                },
                {
                    "controlled_info": [
                        "Information on how the foreign technology or information is controlled cannot be blank"
                    ]
                },
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
                    "controlled_information": ["Enter details about the ITAR controlled technology or information"],
                    "itar_reference_number": ["Enter an ITAR reference number"],
                    "usml_categories": ["Enter a USML category"],
                    "itar_approval_scope": ["Enter details about the ITAR approval scope"],
                    "expected_time_in_possession": ["Enter how long you'll possess the technology or information"],
                },
            ),
            (
                FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES,
                {},
                {"is_used_by_uk_armed_forces": ["Select yes if UK armed forced will use the item"]},
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
        force_mod_funded,
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
                "email_address": "test@test.com",  # /PS-IGNORE
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
                        "fields": {
                            "product_name": {
                                "key": "product_name",
                                "answer": "Test Name",
                                "raw_answer": "Test Name",
                                "question": "Give the item a descriptive name",
                                "datatype": "string",
                            },
                            "product_description": {
                                "key": "product_description",
                                "answer": "Does a thing",
                                "raw_answer": "Does a thing",
                                "question": "Describe the item",
                                "datatype": "string",
                            },
                            "has_security_classification": {
                                "key": "has_security_classification",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Has the product been given a security classification by a UK MOD authority?",
                                "datatype": "boolean",
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
                                "answer": "Unclassified",
                                "raw_answer": "unclassified",
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
                                "question": "Enter any additional markings (optional)",
                                "datatype": "string",
                            },
                            "issuing_authority_name_address": {
                                "key": "issuing_authority_name_address",
                                "answer": "some address",
                                "raw_answer": "some address",
                                "question": "Name and address of the issuing authority",
                                "datatype": "string",
                            },
                            "reference": {
                                "key": "reference",
                                "answer": "1234",
                                "raw_answer": "1234",
                                "question": "Reference",
                                "datatype": "string",
                            },
                            "date_of_issue": {
                                "key": "date_of_issue",
                                "answer": "2025-01-01",
                                "raw_answer": "2025-01-01",
                                "question": "Date of issue",
                                "datatype": "date",
                            },
                            "is_foreign_tech_or_information_shared": {
                                "key": "is_foreign_tech_or_information_shared",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Will any foreign technology or information be shared with the item?",
                                "datatype": "boolean",
                            },
                            "is_controlled_under_itar": {
                                "key": "is_controlled_under_itar",
                                "answer": "Yes, it's controlled under  ITAR",
                                "raw_answer": True,
                                "question": "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?",
                                "datatype": "boolean",
                            },
                            "controlled_info": {
                                "key": "controlled_info",
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Explain how the technology or information is controlled.Include countries classification levels and reference numbers.  You can upload supporting documents later in your application",
                                "datatype": "string",
                            },
                            "controlled_information": {
                                "key": "controlled_information",
                                "answer": "secret stuff",
                                "raw_answer": "secret stuff",
                                "question": "What is the ITAR controlled technology or information?",
                                "datatype": "string",
                            },
                            "itar_reference_number": {
                                "key": "itar_reference_number",
                                "answer": "123456",
                                "raw_answer": "123456",
                                "question": "ITAR reference number",
                                "datatype": "string",
                            },
                            "usml_categories": {
                                "key": "usml_categories",
                                "answer": "none",
                                "raw_answer": "none",
                                "question": "What are the United States Munitions List (USML) categories listed on your ITAR approval?",
                                "datatype": "string",
                            },
                            "itar_approval_scope": {
                                "key": "itar_approval_scope",
                                "answer": "no scope",
                                "raw_answer": "no scope",
                                "question": "Describe the scope of your ITAR approval",
                                "datatype": "string",
                            },
                            "expected_time_in_possession": {
                                "key": "expected_time_in_possession",
                                "answer": "10 years",
                                "raw_answer": "10 years",
                                "question": "How long do you expect the technology or information that is controlled under the US ITAR to be in your possession?",
                                "datatype": "string",
                            },
                            "is_including_cryptography_or_security_features": {
                                "key": "is_including_cryptography_or_security_features",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Does the item include cryptography or other information security features?",
                                "datatype": "boolean",
                            },
                            "cryptography_or_security_feature_info": {
                                "key": "cryptography_or_security_feature_info",
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Provide full details",
                                "datatype": "string",
                            },
                            "is_item_rated_under_mctr": {
                                "key": "is_item_rated_under_mctr",
                                "answer": "Yes, the product is MTCR Category 1",
                                "raw_answer": "mtcr_1",
                                "question": "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
                                "datatype": "string",
                            },
                            "is_item_manpad": {
                                "key": "is_item_manpad",
                                "answer": "No, the product is not a MANPAD",
                                "raw_answer": "no",
                                "question": "Do you believe the item is a man-portable air defence system (MANPAD)?",
                                "datatype": "string",
                            },
                            "is_mod_electronic_data_shared": {
                                "key": "is_mod_electronic_data_shared",
                                "answer": "No",
                                "raw_answer": "no",
                                "question": "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?",
                                "datatype": "string",
                            },
                            "funding_source": {
                                "key": "funding_source",
                                "answer": "MOD",
                                "raw_answer": "mod",
                                "question": "Who is funding the item?",
                                "datatype": "string",
                            },
                            "full_name": {
                                "key": "full_name",
                                "answer": "a name",
                                "raw_answer": "a name",
                                "question": "Full name",
                                "datatype": "string",
                            },
                            "address": {
                                "key": "address",
                                "answer": "16 Street",
                                "raw_answer": "16 Street",
                                "question": "Address",
                                "datatype": "string",
                            },
                            "phone_number": {
                                "key": "phone_number",
                                "answer": "01234785785",
                                "raw_answer": "01234785785",
                                "question": "Phone number",
                                "datatype": "string",
                            },
                            "email_address": {
                                "key": "email_address",
                                "answer": "test@test.com",  # /PS-IGNORE
                                "raw_answer": "test@test.com",  # /PS-IGNORE
                                "question": "Email address",
                                "datatype": "string",
                            },
                            "is_used_by_uk_armed_forces": {
                                "key": "is_used_by_uk_armed_forces",
                                "answer": "Yes",
                                "raw_answer": True,
                                "question": "Will the item be used by the UK Armed Forces?",
                                "datatype": "boolean",
                            },
                            "used_by_uk_armed_forces_info": {
                                "key": "used_by_uk_armed_forces_info",
                                "answer": "some info",
                                "raw_answer": "some info",
                                "question": "Explain how it will be used",
                                "datatype": "string",
                            },
                        },
                        "fields_sequence": [
                            "product_name",
                            "product_description",
                            "has_security_classification",
                            "prefix",
                            "security_classification",
                            "other_security_classification",
                            "suffix",
                            "issuing_authority_name_address",
                            "reference",
                            "date_of_issue",
                            "is_foreign_tech_or_information_shared",
                            "is_controlled_under_itar",
                            "controlled_info",
                            "controlled_information",
                            "itar_reference_number",
                            "usml_categories",
                            "itar_approval_scope",
                            "expected_time_in_possession",
                            "is_including_cryptography_or_security_features",
                            "cryptography_or_security_feature_info",
                            "is_item_rated_under_mctr",
                            "is_item_manpad",
                            "is_mod_electronic_data_shared",
                            "funding_source",
                            "full_name",
                            "address",
                            "phone_number",
                            "email_address",
                            "is_used_by_uk_armed_forces",
                            "used_by_uk_armed_forces_info",
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
        "step, data, required_field, expected_errors",
        (
            (
                FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR,
                {"is_controlled_under_itar": False, "controlled_info": ""},
                "controlled_info",
                ["Information on how the foreign technology or information is controlled cannot be blank"],
            ),
            (
                FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY,
                {"is_including_cryptography_or_security_features": True, "cryptography_or_security_feature_info": ""},
                "cryptography_or_security_feature_info",
                ["Details about the information security features cannot be blank"],
            ),
            (
                FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES,
                {"is_used_by_uk_armed_forces": True, "used_by_uk_armed_forces_info": ""},
                "used_by_uk_armed_forces_info",
                ["Details about how the item will be used cannot be blank"],
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
        expected_errors,
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

        assert response.context["form"][required_field].errors == expected_errors
