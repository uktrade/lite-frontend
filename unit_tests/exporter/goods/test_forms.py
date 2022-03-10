from unittest.mock import patch

import pytest
import requests
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.core.services import get_pv_gradings
from exporter.applications.services import serialize_good_on_app_data
from exporter.goods import forms
from lite_content.lite_exporter_frontend.goods import CreateGoodForm


@pytest.fixture(autouse=True)
def setup(
    mock_control_list_entries,
    mock_pv_gradings,
):
    yield


def post_request(rf, client, data=None):
    request = rf.post("/", data if data else {})
    request.session = client.session
    request.requests_session = requests.Session()
    return request


@pytest.mark.parametrize(
    "value, serialized",
    [
        ("2,300.00", "2300.00"),
        ("2,3,,,,,00.00", "2300.00"),
        ("23,444200", "23444200"),
        ("foo", "foo"),  # this will be caught by serializer on the api and return an error
        ("84.34.111", "84.34.111"),  # this too
    ],
)
def test_serialize_good_on_app_data(value, serialized):
    data = {
        "good_id": "some-uuid",
        "value": value,
        "quantity": value,
    }
    expected = {
        "good_id": "some-uuid",
        "value": serialized,
        "quantity": serialized,
    }
    assert serialize_good_on_app_data(data) == expected


@pytest.mark.parametrize(
    "value, serialized",
    [
        ("2,300.00", "2300.00"),
        ("2,3,,,,,00.00", "2300.00"),
        ("23,444200", "23444200"),
        ("foo", "foo"),  # this will be caught by serializer on the api and return an error
        ("84.34.111", "84.34.111"),  # this too
    ],
)
def test_serialize_good_on_app_data_no_value_key(value, serialized):

    data = {
        "good_id": "some-uuid",
        "quantity": value,
    }
    expected = {
        "good_id": "some-uuid",
        "quantity": serialized,
    }
    assert serialize_good_on_app_data(data) == expected


@pytest.fixture
def pv_gradings(mock_pv_gradings, rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    data = get_pv_gradings(request, convert_to_options=True)
    return data


def test_has_valid_section_five_certificate_is_expired():
    actual = forms.has_valid_section_five_certificate(
        {"organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": True}]}}
    )

    assert actual is False


def test_has_valid_section_five_certificate_not_expired():
    actual = forms.has_valid_section_five_certificate(
        {"organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": False}]}}
    )

    assert actual is True


def test_has_valid_section_five_certificate_empty():
    actual = forms.has_valid_section_five_certificate({"organisation": {"documents": []}})

    assert actual is False


def test_goods_check_document_available_form():
    form = forms.check_document_available_form("back")
    assert len(form.questions) == 1
    assert form.title == "Do you have a document that shows what your product is and what it’s designed to do?"
    assert form.description
    assert form.questions[0].name == "is_document_available"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Continue"


def test_goods_check_document_sensitivity_form():
    form = forms.document_grading_form("back")
    assert len(form.questions) == 1
    assert form.title == "Is the document rated above OFFICIAL-SENSITIVE?"
    assert form.questions[0].name == "is_document_sensitive"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Save and continue"


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"item_category": "group2_firearms"}, True),
        ({"instructions_to_exporter": ""}, False),
    ),
)
def test_product_category_form(data, valid):
    form = forms.ProductCategoryForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors["item_category"][0] == "Select a product category"


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"type": "firearms"}, True),
        ({"type": ""}, False),
    ),
)
def test_group_two_product_type_form(data, valid):
    form = forms.GroupTwoProductTypeForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["product_type_step"]

    if not valid:
        assert form.errors["type"][0] == "Select the type of product"


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        ({"number_of_items": "3"}, True, None, None),
        ({"number_of_items": ""}, False, "number_of_items", "Enter the number of items"),
        ({"number_of_items": "foo"}, False, "number_of_items", "Enter a whole number."),
    ),
)
def test_firearms_number_of_items_form(data, valid, error_field, error_message):
    form = forms.FirearmsNumberOfItemsForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["number_of_items_step"]

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        (
            {},
            False,
            {
                "serial_numbers_available": [
                    "Select whether you can enter serial numbers now, later or if the product does not have them"
                ]
            },
        ),
        (
            {"serial_numbers_available": "AVAILABLE"},
            True,
            {},
        ),
        (
            {"serial_numbers_available": "LATER"},
            True,
            {},
        ),
        (
            {"serial_numbers_available": "NOT_AVAILABLE", "no_identification_markings_details": "test details"},
            True,
            {},
        ),
        (
            {"serial_numbers_available": "NOT_AVAILABLE", "no_identification_markings_details": ""},
            False,
            {"no_identification_markings_details": ["Enter a reason why the product has not been marked"]},
        ),
    ),
)
def test_identification_markings_form(data, valid, errors):
    form = forms.IdentificationMarkingsForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["identification_markings_step"]
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, cleaned_data, errors",
    (
        (
            {"serial_numbers_0": "abc", "serial_numbers_1": "def", "serial_numbers_2": "ghi"},
            True,
            {
                "serial_number_input_0": "abc",
                "serial_number_input_1": "def",
                "serial_number_input_2": "ghi",
                "capture_serial_numbers_step": True,
            },
            {},
        ),
        (
            {"serial_numbers_0": "", "serial_numbers_1": "", "serial_numbers_2": ""},
            False,
            {"capture_serial_numbers_step": True},
            {"serial_numbers": ["Enter at least one serial number"]},
        ),
    ),
)
def test_firearms_capture_serial_numbers_form(data, valid, cleaned_data, errors):
    form = forms.FirearmsCaptureSerialNumbersForm(data=data, number_of_items=3)

    assert form.is_valid() == valid
    assert form.cleaned_data == cleaned_data
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, cleaned_data, errors",
    (
        (
            {"serial_numbers_0": "abc", "serial_numbers_1": "def", "serial_numbers_2": "ghi"},
            True,
            {"serial_number_input_0": "abc", "serial_number_input_1": "def", "serial_number_input_2": "ghi"},
            {},
        ),
        (
            {"serial_numbers_0": "", "serial_numbers_1": "", "serial_numbers_2": ""},
            False,
            {},
            {"serial_numbers": ["Enter at least one serial number"]},
        ),
    ),
)
def test_update_serial_numbers_form(data, valid, cleaned_data, errors):
    form = forms.UpdateSerialNumbersForm(data=data, number_of_items=3, product_name="test product name")

    assert form.is_valid() == valid
    assert form.cleaned_data == cleaned_data
    assert form.errors == errors
    assert form.title == "Enter the serial numbers for 'test product name'"


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"is_military_use": "yes_designed"}, True),
        ({"is_military_use": "yes_modified", "modified_military_use_details": "details"}, True),
        ({"is_military_use": ""}, False),
        ({"is_military_use": "yes_modified", "modified_military_use_details": ""}, False),
    ),
)
def test_product_military_use_form(data, valid):
    form = forms.ProductMilitaryUseForm(data=data)

    assert form.is_valid() == valid

    if not data.get("is_military_use"):
        assert not valid and form.errors["is_military_use"][0] == "Select no if the product is not for military use"
    elif data["is_military_use"] == "yes_modified" and not data["modified_military_use_details"]:
        assert not valid and form.errors["modified_military_use_details"][0] == "Enter the details of the modifications"


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"uses_information_security": "True"}, True),
        ({"uses_information_security": ""}, False),
    ),
)
def test_product_uses_information_security_form(data, valid):
    form = forms.ProductUsesInformationSecurityForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert (
            form.errors["uses_information_security"][0]
            == "Select yes if the product is designed to employ information security features"
        )


@pytest.mark.parametrize(
    "data, application_pk, valid, error_field, error_message",
    (
        (
            {
                "name": "test name",
                "description": "test desc",
                "part_number": "part_no",
                "is_good_controlled": "True",
                "control_list_entries": ["ML1", "ML1a"],
                "is_pv_graded": "yes",
            },
            "12345",
            True,
            None,
            None,
        ),
        (
            {
                "name": "test name",
                "description": "test desc",
                "part_number": "part_no",
                "is_good_controlled": "False",
                "control_list_entries": ["ML1", "ML1a"],
                "is_pv_graded": "yes",
            },
            None,
            True,
            None,
            None,
        ),
        (
            {
                "name": "",
                "description": "test desc",
                "part_number": "part_no",
                "is_good_controlled": "True",
                "control_list_entries": ["ML1", "ML1a"],
                "is_pv_graded": "yes",
            },
            None,
            False,
            "name",
            "Enter a product name",
        ),
        (
            {
                "name": "test name",
                "description": "test desc",
                "part_number": "part_no",
                "is_good_controlled": "",
                "control_list_entries": ["ML1", "ML1a"],
                "is_pv_graded": "yes",
            },
            None,
            False,
            "is_good_controlled",
            "This field is required.",
        ),
        (
            {
                "name": "test name",
                "description": "test desc",
                "part_number": "part_no",
                "is_good_controlled": "True",
                "control_list_entries": ["ML1", "ML1a"],
                "is_pv_graded": "",
            },
            None,
            False,
            "is_pv_graded",
            "Select an option",
        ),
    ),
)
def test_add_goods_questions_form(rf, client, data, application_pk, valid, error_field, error_message):
    request = post_request(rf, client)
    request.session["clc_list"] = [{"rating": "ML1"}, {"rating": "ML1a"}]

    form = forms.AddGoodsQuestionsForm(data=data, application_pk=application_pk, request=request)

    assert form.is_valid() == valid
    if application_pk is not None:
        assert form.title == CreateGoodForm.TITLE_APPLICATION
    else:
        assert form.title == CreateGoodForm.TITLE_GOODS_LIST
    assert form.fields["control_list_entries"].choices == [("ML1", "ML1"), ("ML1a", "ML1a")]
    if data["is_good_controlled"] == "False":
        assert valid and "control_list_entries" not in form.cleaned_data

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        (
            {
                "prefix": "test prefix",
                "grading": "key1",
                "suffix": "test suffix",
                "custom_grading": "",
                "issuing_authority": "test authority",
                "reference": "test ref",
                "date_of_issue_0": 1,
                "date_of_issue_1": 1,
                "date_of_issue_2": 2021,
            },
            True,
            None,
            None,
        ),
        (
            {
                "prefix": "test prefix",
                "grading": "key1",
                "suffix": "test suffix",
                "custom_grading": "",
                "issuing_authority": "",
                "reference": "test ref",
                "date_of_issue_0": 1,
                "date_of_issue_1": 1,
                "date_of_issue_2": 2021,
            },
            False,
            "issuing_authority",
            "This field may not be blank",
        ),
        (
            {
                "prefix": "test prefix",
                "grading": "key1",
                "suffix": "test suffix",
                "custom_grading": "custom_grading",
                "issuing_authority": "test authority",
                "reference": "test ref",
                "date_of_issue_0": 1,
                "date_of_issue_1": 1,
                "date_of_issue_2": 2021,
            },
            False,
            "custom_grading",
            "Check if this grading or the grading selected on the dropdown list is the correct one for the product",
        ),
    ),
)
@patch("exporter.goods.forms.get_pv_gradings")
def test_pv_details_form(mock_get_pv_gradings, data, valid, error_field, error_message):
    mock_get_pv_gradings.return_value = [{"key1": "display1"}, {"key2": "display2"}]

    form = forms.PvDetailsForm(data=data, request="test request")

    assert form.is_valid() == valid
    assert form.fields["grading"].choices == [("", "Select"), ("key1", "display1"), ("key2", "display2")]
    mock_get_pv_gradings.assert_called_once_with("test request")

    if valid:
        assert form.cleaned_data["date_of_issue"] == "2021-01-01"
        assert form.cleaned_data["date_of_issueday"] == "1"
        assert form.cleaned_data["date_of_issuemonth"] == "1"
        assert form.cleaned_data["date_of_issueyear"] == "2021"
    else:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, error_message",
    (
        ({"year_of_manufacture": "2010"}, True, None),
        ({"year_of_manufacture": ""}, False, "Enter the year of manufacture"),
        ({"year_of_manufacture": "X"}, False, "Year of manufacture must be valid"),
        ({"year_of_manufacture": "-1"}, False, "Year of manufacture must be valid"),
        ({"year_of_manufacture": "2200"}, False, "Year of manufacture must be in the past"),
    ),
)
def test_firearms_year_of_manufacture_details_form(data, valid, error_message):
    form = forms.FirearmsYearOfManufactureDetailsForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert error_message in form.errors["year_of_manufacture"]


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        ({"is_replica": "True", "replica_description": "test desc"}, True, None, None),
        ({"is_replica": ""}, False, "is_replica", "Select yes if the product is a replica firearm"),
        ({"is_replica": "True", "replica_description": ""}, False, "replica_description", "Enter a description"),
    ),
)
def test_firearms_replica_form_form(data, valid, error_field, error_message):
    form = forms.FirearmsReplicaForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["is_replica_step"]

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        ({"calibre": "22"}, True, None, None),
        ({"calibre": ""}, False, "calibre", "Enter the calibre"),
    ),
)
def test_firearms_calibre_details_form(data, valid, error_field, error_message):
    form = forms.FirearmsCalibreDetailsForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["firearm_calibre_step"]

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        ({"is_registered_firearm_dealer": "True"}, True, None, None),
        (
            {"is_registered_firearm_dealer": ""},
            False,
            "is_registered_firearm_dealer",
            "Select yes if you are a registered firearms dealer",
        ),
    ),
)
def test_registered_firearms_dealer_form(data, valid, error_field, error_message):
    form = forms.RegisteredFirearmsDealerForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, files, valid, error_field, error_message",
    (
        (
            {"reference_code": "ref_code", "expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2025},
            {"file": SimpleUploadedFile("test", b"test_content")},
            True,
            None,
            None,
        ),
        (
            {"reference_code": "ref_code", "expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2025},
            {"file": ""},
            False,
            "file",
            "Select certificate file to upload",
        ),
        (
            {"reference_code": "", "expiry_date_0": 1, "expiry_date_1": 1, "expiry_date_2": 2025},
            {"file": SimpleUploadedFile("test", b"test_content")},
            False,
            "reference_code",
            "Enter the certificate number",
        ),
        (
            {"reference_code": "ref_code", "expiry_date_0": "", "expiry_date_1": "", "expiry_date_2": ""},
            {"file": SimpleUploadedFile("test", b"test_content")},
            False,
            "expiry_date",
            "Enter the day, month and year",
        ),
        (
            {"reference_code": "ref_code", "expiry_date_0": "1", "expiry_date_1": "1", "expiry_date_2": "2020"},
            {"file": SimpleUploadedFile("test", b"test_content")},
            False,
            "expiry_date",
            "Expiry date must be in the future",
        ),
    ),
)
def test_attach_fiream_dealer_certificate_form(data, files, valid, error_field, error_message):
    form = forms.AttachFirearmsDealerCertificateForm(data=data, files=files)

    assert form.is_valid() == valid

    if valid:
        assert form.cleaned_data["expiry_date_day"] == "1"
        assert form.cleaned_data["expiry_date_month"] == "1"
        assert form.cleaned_data["expiry_date_year"] == "2025"
    else:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, is_rfd, valid, error_field, error_message",
    (
        (
            {"is_covered_by_firearm_act_section_one_two_or_five": "Yes", "firearms_act_section": ""},
            True,
            True,
            None,
            None,
        ),
        (
            {"is_covered_by_firearm_act_section_one_two_or_five": "", "firearms_act_section": ""},
            True,
            False,
            "is_covered_by_firearm_act_section_one_two_or_five",
            "Select yes if the product covered by section 5 of the Firearms Act 1968",
        ),
        (
            {"is_covered_by_firearm_act_section_one_two_or_five": "", "firearms_act_section": ""},
            False,
            False,
            "is_covered_by_firearm_act_section_one_two_or_five",
            "Select yes if the product is covered by Section 1, Section 2 or Section 5 of the Firearms Act 1968",
        ),
        (
            {"is_covered_by_firearm_act_section_one_two_or_five": "Yes", "firearms_act_section": ""},
            False,
            False,
            "firearms_act_section",
            "Select which section the product is covered by",
        ),
    ),
)
def test_firearms_act_confirmation_form(data, is_rfd, valid, error_field, error_message):
    form = forms.FirearmsActConfirmationForm(data=data, is_rfd=is_rfd)

    assert form.is_valid() == valid
    assert form.cleaned_data["section_certificate_step"]

    if not valid:
        assert form.errors[error_field][0] == error_message

    if is_rfd:
        assert form.title == "Is the product covered by section 5 of the Firearms Act 1968?"
    else:
        assert form.title == CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE


@pytest.mark.parametrize(
    "data, product_type, valid, error_field, error_message",
    (
        ({"software_or_technology_details": "Some details"}, "group3_software", True, None, None),
        (
            {"software_or_technology_details": ""},
            "group3_software",
            False,
            "software_or_technology_details",
            "Enter the purpose of the software",
        ),
        (
            {"software_or_technology_details": ""},
            "group3_technology",
            False,
            "software_or_technology_details",
            "Enter the purpose of the technology",
        ),
    ),
)
def test_software_technology_details_form(data, product_type, valid, error_field, error_message):
    form = forms.SoftwareTechnologyDetailsForm(product_type=product_type, data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, error_field, error_message",
    (
        ({"is_component": "yes_designed", "designed_details": "Test details"}, True, None, None),
        ({"is_component": ""}, False, "is_component", "Select no if the product is not a component"),
        (
            {"is_component": "yes_designed", "designed_details": ""},
            False,
            "designed_details",
            "Enter the details of the hardware",
        ),
        (
            {"is_component": "yes_modified", "modified_details": ""},
            False,
            "modified_details",
            "Enter the details of the modifications and the hardware",
        ),
        (
            {"is_component": "yes_general", "general_details": ""},
            False,
            "general_details",
            "Enter the details of the types of applications the component is intended to be used in",
        ),
        (
            {"is_component": "yes_designed", "designed_details": "x" * 2001},
            False,
            "designed_details",
            "Ensure this field has no more than 2000 characters",
        ),
        (
            {"is_component": "yes_modified", "modified_details": "x" * 2001},
            False,
            "modified_details",
            "Ensure this field has no more than 2000 characters",
        ),
        (
            {"is_component": "yes_general", "general_details": "x" * 2001},
            False,
            "general_details",
            "Ensure this field has no more than 2000 characters",
        ),
    ),
)
def test_product_component_form(data, valid, error_field, error_message):
    form = forms.ProductComponentForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        (
            {},
            False,
            {
                "has_proof_mark": ["Select whether the product has valid UK proof marks"],
                "is_deactivated": ["Select yes if the product has been deactivated"],
                "is_good_incorporated": ["Select yes if the product will be incorporated into another product"],
                "value": ["Enter the total value of the products"],
            },
        ),
        (
            {
                "has_proof_mark": True,
                "is_deactivated": True,
                "is_good_incorporated": True,
                "value": "150",
            },
            False,
            {
                "date_of_deactivation": ["Enter a valid date of deactivation"],
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK/EU proof house standards"
                ],
            },
        ),
        (
            {
                "has_proof_mark": True,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "value": "150",
            },
            False,
            {
                "deactivation_standard": ["Select yes if the product has valid UK proof marks"],
            },
        ),
        (
            {
                "has_proof_mark": True,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard": "UK",
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "value": "150",
            },
            True,
            {},
        ),
        (
            {
                "has_proof_mark": True,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_deactivated_to_standard": False,
                "is_good_incorporated": True,
                "value": "150",
            },
            False,
            {
                "deactivation_standard_other": [
                    "Enter details of who deactivated the product and to what standard it was done"
                ]
            },
        ),
        (
            {
                "has_proof_mark": True,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard_other": "other",
                "is_deactivated_to_standard": False,
                "is_good_incorporated": True,
                "value": "150",
            },
            True,
            {},
        ),
        (
            {
                "has_proof_mark": False,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard_other": "other",
                "is_deactivated_to_standard": False,
                "is_good_incorporated": True,
                "value": "150",
            },
            False,
            {"no_proof_mark_details": ["Enter details of why the product does not have valid UK proof marks"]},
        ),
        (
            {
                "has_proof_mark": False,
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard_other": "other",
                "is_deactivated_to_standard": False,
                "is_good_incorporated": True,
                "no_proof_mark_details": "no proof mark details",
                "value": "150",
            },
            True,
            {},
        ),
    ),
)
def test_firearms_unit_quantity_value_form(data, valid, errors):
    good = {
        "name": "good name",
        "control_list_entries": [],
        "part_number": "",
        "item_category": {
            "key": "",
        },
    }

    form = forms.FirearmsUnitQuantityValueForm(data=data, good=good)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        (
            {},
            False,
            {
                "is_deactivated": ["Select yes if the product has been deactivated"],
                "is_good_incorporated": ["Select yes if the product will be incorporated into another product"],
                "is_gun_barrel": ["Select whether the product is a gun barrel or the action of a gun"],
                "value": ["Enter the total value of the products"],
            },
        ),
        (
            {
                "is_deactivated": True,
                "is_good_incorporated": True,
                "is_gun_barrel": False,
                "value": "150",
            },
            False,
            {
                "date_of_deactivation": ["Enter a valid date of deactivation"],
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK/EU proof house standards"
                ],
            },
        ),
        (
            {
                "is_deactivated": True,
                "is_good_incorporated": True,
                "is_gun_barrel": False,
                "value": "150",
            },
            False,
            {
                "date_of_deactivation": ["Enter a valid date of deactivation"],
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK/EU proof house standards"
                ],
            },
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_good_incorporated": True,
                "is_gun_barrel": False,
                "value": "150",
            },
            False,
            {
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK/EU proof house standards"
                ],
            },
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "is_gun_barrel": False,
                "value": "150",
            },
            False,
            {"deactivation_standard": ["Select yes if the product has valid UK proof marks"]},
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard": "UK",
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "is_gun_barrel": False,
                "value": "150",
            },
            True,
            {},
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard": "UK",
                "has_proof_mark": False,
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "is_gun_barrel": True,
                "value": "150",
            },
            False,
            {"no_proof_mark_details": ["Enter details of why the product does not have valid UK proof marks"]},
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard": "UK",
                "has_proof_mark": False,
                "is_deactivated_to_standard": True,
                "is_good_incorporated": True,
                "is_gun_barrel": True,
                "no_proof_mark_details": "no proof mark details",
                "value": "150",
            },
            True,
            {},
        ),
    ),
)
def test_component_of_a_firearm_unit_quantity_value_form(data, valid, errors):
    good = {
        "name": "good name",
        "control_list_entries": [],
        "part_number": "",
        "item_category": {
            "key": "",
        },
    }

    form = forms.ComponentOfAFirearmUnitQuantityValueForm(data=data, good=good)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        (
            {},
            False,
            {
                "is_deactivated": ["Select yes if the product has been deactivated"],
                "is_good_incorporated": ["Select yes if the product will be incorporated into another product"],
                "value": ["Enter the total value of the products"],
            },
        ),
        (
            {
                "is_deactivated": True,
                "is_good_incorporated": True,
                "value": "150",
            },
            False,
            {
                "date_of_deactivation": ["Enter a valid date of deactivation"],
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK/EU proof house standards"
                ],
            },
        ),
        (
            {
                "is_deactivated": True,
                "is_good_incorporated": True,
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_deactivated_to_standard": True,
                "value": "150",
            },
            False,
            {
                "deactivation_standard": ["Select yes if the product has valid UK proof marks"],
            },
        ),
        (
            {
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard": "UK",
                "is_deactivated": True,
                "is_good_incorporated": True,
                "is_deactivated_to_standard": True,
                "value": "150",
            },
            True,
            {},
        ),
        (
            {
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "is_deactivated": True,
                "is_good_incorporated": True,
                "is_deactivated_to_standard": False,
                "value": "150",
            },
            False,
            {
                "deactivation_standard_other": [
                    "Enter details of who deactivated the product and to what standard it was done"
                ]
            },
        ),
        (
            {
                "date_of_deactivation_0": "1",
                "date_of_deactivation_1": "2",
                "date_of_deactivation_2": "2020",
                "deactivation_standard_other": "other",
                "is_deactivated": True,
                "is_good_incorporated": True,
                "is_deactivated_to_standard": False,
                "value": "150",
            },
            True,
            {},
        ),
    ),
)
def test_component_of_a_firearm_ammunition_unit_quantity_value_form(data, valid, errors):
    good = {
        "name": "good name",
        "control_list_entries": [],
        "part_number": "",
        "item_category": {
            "key": "",
        },
    }

    form = forms.ComponentOfAFirearmAmmunitionUnitQuantityValueForm(data=data, good=good)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        (
            {},
            False,
            {
                "is_good_incorporated": ["Select yes if the product will be incorporated into another product"],
                "quantity": ["Enter a quantity"],
                "unit": ["Select a unit of measurement"],
                "value": ["Enter the total value of the products"],
            },
        ),
        (
            {
                "is_good_incorporated": True,
                "quantity": "100",
                "unit": "GRM",
                "value": "150",
            },
            True,
            {},
        ),
        ({"is_good_incorporated": True, "unit": "ITG"}, True, {}),
    ),
)
def test_unit_quantity_value_form(rf, client, mock_units, data, valid, errors):
    good = {
        "name": "good name",
        "control_list_entries": [],
        "part_number": "",
        "item_category": {
            "key": "",
        },
    }

    request = post_request(rf, client)

    form = forms.UnitQuantityValueForm(data=data, good=good, request=request)
    assert form.fields["unit"].choices == [
        ("", "Select"),
        ("GRM", "Gram(s)"),
        ("KGM", "Kilogram(s)"),
        ("NAR", "Number of articles"),
        ("MTK", "Square metre(s)"),
        ("MTR", "Metre(s)"),
        ("LTR", "Litre(s)"),
        ("MTQ", "Cubic metre(s)"),
        ("ITG", "Intangible"),
    ]

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors
