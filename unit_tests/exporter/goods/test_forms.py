from unittest.mock import patch

import pytest
import requests
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, RequestFactory

from exporter.core.constants import PRODUCT_CATEGORY_FIREARM
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


def test_add_goods_questions_feature_flag():
    form = forms.add_goods_questions(control_list_entries=[])
    assert len(form.questions[3].options) == 2
    assert form.questions[3].options[-1].key == False
    assert form.questions[3].options[-1].value == "No"
    assert len(form.questions[4].options) == 2
    assert form.questions[4].options[-1].key == "no"
    assert form.questions[4].options[-1].value == "No, it doesn't need one"


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


@pytest.mark.parametrize(
    "params, num_forms, question_checks",
    [
        (
            {"is_firearm_ammunition_or_component": True},
            4,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
            ],
        ),
        (
            {"is_firearm_ammunition_or_component": True, "draft_pk": "123", "is_firearm": True},
            9,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 2, "name": "number_of_items"},
                {"qindex": 1, "name": "has_identification_markings"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "year_of_manufacture"},
                {"qindex": 2, "name": "is_replica"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
                {"qindex": 2, "name": "is_covered_by_firearm_act_section_one_two_or_five"},
            ],
        ),
        (
            {"is_firearm_ammunition_or_component": True, "draft_pk": "123", "is_firearm": False},
            7,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 2, "name": "number_of_items"},
                {"qindex": 1, "name": "has_identification_markings"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "calibre"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
                {"qindex": 2, "name": "is_covered_by_firearm_act_section_one_two_or_five"},
            ],
        ),
        (
            {"is_firearms_accessory": True},
            5,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "is_component"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
        (
            {"is_firearms_software_or_tech": True},
            5,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "software_or_technology_details"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
    ],
)
@override_settings(FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS=True)
def test_core_firearm_product_form_group(rf, client, params, num_forms, question_checks):
    """Test to ensure correct set of questions are asked in adding a firearm product journey depending on the firearm_type."""
    kwargs = {"is_pv_graded": False, **params}
    request = post_request(rf, client, data={})
    form_parts = forms.add_good_form_group(request, **kwargs).forms
    assert len(set(form_parts)) == len(form_parts)
    assert len(form_parts) == int(num_forms), list(map(str, form_parts))

    for i, q in enumerate(question_checks):
        assert form_parts[i].questions[q["qindex"]].name == q["name"]


@pytest.mark.parametrize(
    "params, num_forms, question_checks",
    [
        (
            {"is_firearm_ammunition_or_component": True},
            5,
            [
                {"qindex": 0, "name": "item_category"},
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
            ],
        ),
        (
            {"is_firearm_ammunition_or_component": True, "draft_pk": "123", "is_firearm": True},
            10,
            [
                {"qindex": 0, "name": "item_category"},
                {"qindex": 1, "name": "type"},
                {"qindex": 2, "name": "number_of_items"},
                {"qindex": 1, "name": "has_identification_markings"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "year_of_manufacture"},
                {"qindex": 2, "name": "is_replica"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
                {"qindex": 2, "name": "is_covered_by_firearm_act_section_one_two_or_five"},
            ],
        ),
        (
            {"is_firearm_ammunition_or_component": True, "draft_pk": "123", "is_firearm": False},
            8,
            [
                {"qindex": 0, "name": "item_category"},
                {"qindex": 1, "name": "type"},
                {"qindex": 2, "name": "number_of_items"},
                {"qindex": 1, "name": "has_identification_markings"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "calibre"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
                {"qindex": 2, "name": "is_covered_by_firearm_act_section_one_two_or_five"},
            ],
        ),
        (
            {"is_firearms_accessory": True},
            6,
            [
                {"qindex": 0, "name": "item_category"},
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "is_component"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
        (
            {"is_firearms_software_or_tech": True},
            6,
            [
                {"qindex": 0, "name": "item_category"},
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "software_or_technology_details"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
    ],
)
@override_settings(FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS=False)
def test_core_firearm_product_form_group_firearms_feature_off(rf, client, params, num_forms, question_checks):
    """Test to ensure correct set of questions are asked in adding a firearm product journey depending on the firearm_type."""
    kwargs = {"is_pv_graded": False, **params}
    request = post_request(rf, client, data={"item_category": PRODUCT_CATEGORY_FIREARM})
    form_parts = forms.add_good_form_group(request, **kwargs).forms
    assert len(set(form_parts)) == len(form_parts)
    assert len(form_parts) == int(num_forms), list(map(str, form_parts))

    for i, q in enumerate(question_checks):
        assert form_parts[i].questions[q["qindex"]].name == q["name"]


def test_has_valid_rfd_certificate_is_expired():
    actual = forms.has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": True}]}}
    )

    assert actual is False


def test_has_valid_rfd_certificate_not_expired():
    actual = forms.has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": False}]}}
    )

    assert actual is True


def test_has_valid_rfd_certificate_empty():
    actual = forms.has_valid_rfd_certificate({"organisation": {"documents": []}})

    assert actual is False


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


def test_goods_firearms_number_of_items_form():
    form = forms.firearms_number_of_items("firearms")
    assert len(form.questions) == 3
    assert form.title == "Number of items"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Continue"


def test_goods_firearms_capture_serial_numbers_form():
    number_of_items = 5
    form = forms.firearms_capture_serial_numbers(number_of_items)
    assert len(form.questions) == 4
    # number of input fields + label
    assert len(form.questions[3].components) == (number_of_items + 1)
    assert form.title == "Enter the serial numbers for this product"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Save and continue"


@pytest.mark.parametrize(
    "data, valid", (({"item_category": "group2_firearms"}, True), ({"instructions_to_exporter": ""}, False),),
)
def test_product_category_form(data, valid):
    form = forms.ProductCategoryForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors["item_category"][0] == "Select a product category"


@pytest.mark.parametrize(
    "data, valid", (({"type": "firearms"}, True), ({"type": ""}, False),),
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
    "data, valid, error_field, error_message",
    (
        ({"has_identification_markings": "True"}, True, None, None),
        (
            {"has_identification_markings": "False", "no_identification_markings_details": "test details"},
            True,
            None,
            None,
        ),
        (
            {"has_identification_markings": "False", "no_identification_markings_details": ""},
            False,
            "no_identification_markings_details",
            "Enter a reason why the product has not been marked",
        ),
        (
            {"has_identification_markings": ""},
            False,
            "has_identification_markings",
            "Select yes if the product has identification markings",
        ),
    ),
)
def test_identification_markings_form(data, valid, error_field, error_message):
    form = forms.IdentificationMarkingsForm(data=data)

    assert form.is_valid() == valid
    assert form.cleaned_data["identification_markings_step"]

    if not valid:
        assert form.errors[error_field][0] == error_message


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"serial_number_input_0": "abc", "serial_number_input_1": "def", "serial_number_input_2": "ghi"}, True),
        ({"serial_number_input_0": "", "serial_number_input_1": "", "serial_number_input_2": ""}, False),
    ),
)
def test_firearms_capture_serial_numbers_form(data, valid):
    form = forms.FirearmsCaptureSerialNumbersForm(data=data, number_of_items=3)

    assert form.is_valid() == valid
    assert form.cleaned_data["capture_serial_numbers_step"]

    if not valid:
        assert form.errors["__all__"][0] == "Enter at least one serial number"


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

    if "is_military_use" not in data:
        assert not valid and form.errors["is_military_use"][0] == "Select an option"
    elif data["is_military_use"] == "yes_modified" and not data["modified_military_use_details"]:
        assert not valid and form.errors["modified_military_use_details"][0] == "Enter the details of the modifications"


@pytest.mark.parametrize(
    "data, valid", (({"uses_information_security": "True"}, True), ({"uses_information_security": ""}, False),),
)
def test_product_uses_information_security_form(data, valid):
    form = forms.ProductUsesInformationSecurityForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors["uses_information_security"][0] == "Select an option"


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
            "Select an option",
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
def test_add_goods_questions_form(data, application_pk, valid, error_field, error_message):
    request = RequestFactory().get("/")
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    request.session["clc_list"] = [{"rating": "ML1"}, {"rating": "ML1a"}]

    form = forms.AddGoodsQuestionsForm(data=data, application_pk=application_pk, request=request,)

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
        ({"is_replica": ""}, False, "is_replica", "Select an option"),
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
    (({"calibre": "22"}, True, None, None), ({"calibre": ""}, False, "calibre", "Enter the calibre"),),
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
        ({"is_registered_firearm_dealer": ""}, False, "is_registered_firearm_dealer", "Select an option"),
    ),
)
def test_firearms_calibre_details_form(data, valid, error_field, error_message):
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
            "Select an option",
        ),
        (
            {"is_covered_by_firearm_act_section_one_two_or_five": "Yes", "firearms_act_section": ""},
            False,
            False,
            "firearms_act_section",
            "Select an option",
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
    "data, valid, error_field, error_message",
    (
        ({"is_component": "yes_designed"}, True, None, None),
        ({"is_component": ""}, False, "is_component", "Select an option"),
    ),
)
def test_product_component_form(data, valid, error_field, error_message):
    form = forms.ProductComponentForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors[error_field][0] == error_message
