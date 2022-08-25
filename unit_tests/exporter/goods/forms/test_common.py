import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.goods.forms.common import (
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductPVGradingDetailsForm,
    ProductNameForm,
    ProductControlListEntryForm,
    ProductPVGradingForm,
    ProductPartNumberForm,
    ProductQuantityAndValueForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_product_form(data, is_valid, errors):
    form = ProductNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


def test_product_control_list_entry_form_init_control_list_entries(request_with_session, control_list_entries):
    form = ProductControlListEntryForm(request=request_with_session)
    assert form.fields["control_list_entries"].choices == [("ML1", "ML1"), ("ML1a", "ML1a")]


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_good_controlled": ["Select yes if you know the product's control list entry"]}),
        ({"is_good_controlled": True}, False, {"control_list_entries": ["Enter the control list entry"]}),
        ({"is_good_controlled": True, "control_list_entries": ["ML1", "ML1a"]}, True, {}),
        ({"is_good_controlled": False}, True, {}),
    ),
)
def test_product_control_list_entry_form(data, is_valid, errors, request_with_session, control_list_entries):
    form = ProductControlListEntryForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_pv_graded": ["Select yes if the product has a security grading or classification"]}),
        ({"is_pv_graded": True}, True, {}),
        ({"is_pv_graded": False}, True, {}),
    ),
)
def test_product_pv_security_gradings_form(data, is_valid, errors):
    form = ProductPVGradingForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "part_number": ["Enter the part number or select that you do not have a part number"],
            },
        ),
        (
            {"part_number_missing": True},
            False,
            {"no_part_number_comments": ["Enter a reason why you do not have a part number"]},
        ),
        (
            {"part_number_missing": True, "no_part_number_comments": ""},
            False,
            {"no_part_number_comments": ["Enter a reason why you do not have a part number"]},
        ),
        (
            {"part_number_missing": True, "part_number": "abc12345"},
            False,
            {"part_number_missing": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False},
            False,
            {"part_number": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False, "no_part_number_comments": "some comments"},
            False,
            {"part_number": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False, "part_number": "abc12345"},
            True,
            {},
        ),
        (
            {"part_number_missing": True, "no_part_number_comments": "some comments"},
            True,
            {},
        ),
    ),
)
def test_product_part_number_form(data, is_valid, errors):
    form = ProductPartNumberForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "grading": ["Select the security grading"],
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "reference": ["Enter the reference"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {"grading": "official", "reference": "ABC123"},
            False,
            {
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month", "Date of issue must include a year"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2040",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be in the past"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "50",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be a real date"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be a real date"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "12",
                "date_of_issue_2": "10000",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be a real date"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            True,
            {},
        ),
    ),
)
def test_product_pv_security_grading_details_form(data, is_valid, errors, request_with_session, pv_gradings):
    form = ProductPVGradingDetailsForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_document_available": ["Select yes or no"]}),
        (
            {"is_document_available": False},
            False,
            {"no_document_comments": ["Enter a reason why you cannot upload a product document"]},
        ),
        ({"is_document_available": False, "no_document_comments": "product not manufactured yet"}, True, {}),
        (
            {"is_document_available": True},
            True,
            {},
        ),
    ),
)
def test_firearm_document_availability_form(data, is_valid, errors):
    form = ProductDocumentAvailabilityForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_document_sensitive": ["Select yes if the document is rated above Official-sensitive"]}),
        ({"is_document_sensitive": True}, True, {}),
        ({"is_document_sensitive": False}, True, {}),
    ),
)
def test_firearm_document_sensitivity_form(data, is_valid, errors):
    form = ProductDocumentSensitivityForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        ({}, {}, False, {"product_document": ["Select a document that shows what your product is designed to do"]}),
        (
            {"description": ""},
            {},
            False,
            {"product_document": ["Select a document that shows what your product is designed to do"]},
        ),
        (
            {"description": "product data sheet"},
            {"product_document": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
    ),
)
def test_firearm_product_document_upload_form(data, files, is_valid, errors):
    form = ProductDocumentUploadForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"number_of_items": ["Enter the number of items"], "value": ["Enter the total value"]}),
        (
            {"number_of_items": "not a number", "value": "100.00"},
            False,
            {"number_of_items": ["Number of items must be a number, like 16"]},
        ),
        (
            {"number_of_items": "1.5", "value": "100.00"},
            False,
            {"number_of_items": ["Number of items must be a number, like 16"]},
        ),
        (
            {"number_of_items": "0", "value": "100.00"},
            False,
            {"number_of_items": ["Number of items must be 1 or more"]},
        ),
        (
            {"number_of_items": "1", "value": "not a number"},
            False,
            {"value": ["Total value must be a number, like 16.32"]},
        ),
        ({"number_of_items": "1", "value": "0"}, False, {"value": ["Total value must be 0.01 or more"]}),
        (
            {"number_of_items": "1", "value": "16.12345"},
            False,
            {"value": ["Total value must not be more than 2 decimals"]},
        ),
        (
            {"number_of_items": "1", "value": "16"},
            True,
            {},
        ),
        (
            {"number_of_items": "1", "value": "16.32"},
            True,
            {},
        ),
    ),
)
def test_product_quantity_and_value(data, is_valid, errors):
    form = ProductQuantityAndValueForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
