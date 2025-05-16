import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDescriptionForm,
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductMilitaryUseForm,
    ProductNameForm,
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPartNumberForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductQuantityAndValueForm,
    ProductUnitQuantityAndValueForm,
    ProductUsesInformationSecurityForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": "TEST NAME"}, True, {}),
        ({"name": "good-!.<>/%&*;+'(),.name"}, True, {}),
        ({"name": "good!name"}, True, {}),
        ({"name": "good-name"}, True, {}),
        ({"name": "test\r\nname"}, True, {}),
        ({"name": "good_name"}, True, {}),
        ({"name": "good$name"}, True, {}),
    ),
)
def test_product_form_validation(data, is_valid, errors):
    form = ProductNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get("/exporter/static/control-list-entries/", json=[{"rating": "ML1"}, {"rating": "ML1a"}])


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
def test_product_control_list_entry_form_validation(data, is_valid, errors, request_with_session, control_list_entries):
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
def test_product_pv_security_gradings_form_validation(data, is_valid, errors):
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
def test_product_part_number_form_validation(data, is_valid, errors):
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
def test_product_pv_security_grading_details_form_validation(data, is_valid, errors, request_with_session, pv_gradings):
    form = ProductPVGradingDetailsForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "is_document_available": [
                    "Select yes if you have a document that shows what your product is and what it’s designed to do"
                ]
            },
        ),
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
def test_firearm_document_availability_form_validation(data, is_valid, errors):
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
def test_firearm_document_sensitivity_form_validation(data, is_valid, errors):
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
def test_firearm_product_document_upload_form_validation(data, files, is_valid, errors):
    form = ProductDocumentUploadForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


def test_product_quantity_and_value_form_fields(render_form, beautiful_soup):
    form = ProductQuantityAndValueForm()
    assert list(form.fields.keys()) == ["number_of_items", "value"]

    rendered = render_form(form)
    soup = beautiful_soup(rendered)
    rendered_fields = [input["name"] for input in soup.select("input:not([type=submit]):not([type=hidden])")]
    assert rendered_fields == ["number_of_items", "value"]


def test_product_quantity_and_value_form_fields_with_request(rf, authorized_client, render_form, beautiful_soup):
    request = rf.get("/")
    request.session = authorized_client.session

    form = ProductQuantityAndValueForm(request=request)
    assert list(form.fields.keys()) == ["number_of_items", "value"]

    rendered = render_form(form)
    soup = beautiful_soup(rendered)
    rendered_fields = [input["name"] for input in soup.select("input:not([type=submit]):not([type=hidden])")]
    assert rendered_fields == ["number_of_items", "value"]


def test_product_quantity_and_value_form_fields_with_request_feature_switch_on(
    rf, authorized_client, settings, organisation_pk, render_form, beautiful_soup
):
    settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = [organisation_pk]

    request = rf.get("/")
    request.session = authorized_client.session

    form = ProductQuantityAndValueForm(request=request)
    assert list(form.fields.keys()) == ["number_of_items", "value", "no_set_quantities_or_value"]

    rendered = render_form(form)
    soup = beautiful_soup(rendered)
    rendered_fields = [input["name"] for input in soup.select("input:not([type=submit]):not([type=hidden])")]
    assert rendered_fields == ["number_of_items", "value", "no_set_quantities_or_value"]


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
def test_product_quantity_and_value_form_validation(data, is_valid, errors):
    form = ProductQuantityAndValueForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"__all__": ["Enter either the quantity and value, or select 'no set quantities or values'"]}),
        (
            {"number_of_items": "1", "value": "16", "no_set_quantities_or_value": True},
            False,
            {"__all__": ["Enter either the quantity and value, or select 'no set quantities or values'"]},
        ),
        (
            {"no_set_quantities_or_value": True},
            True,
            {},
        ),
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
        (
            {"number_of_items": "1"},
            False,
            {"value": ["Enter the total value"]},
        ),
        (
            {"value": "16"},
            False,
            {"number_of_items": ["Enter the number of items"]},
        ),
    ),
)
def test_product_quantity_and_value_form_validation_single_user_journey(
    rf, authorized_client, settings, data, is_valid, errors
):
    settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = ["*"]

    request = rf.get("/")
    request.session = authorized_client.session

    form = ProductQuantityAndValueForm(request=request, data=data)
    assert form.is_valid() == is_valid, form.errors
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "unit": ["Select a unit of measurement"],
                "quantity": ["Enter the quantity"],
                "value": ["Enter the total value"],
            },
        ),
        (
            {"unit": "TON", "quantity": "not a number", "value": "100.00"},
            False,
            {"quantity": ["Quantity must be a number, like 16.32"]},
        ),
        (
            {"unit": "TON", "quantity": "1.1234", "value": "100.00"},
            False,
            {"quantity": ["Quantity must be less than 4 decimal places, like 123.456 or 156"]},
        ),
        (
            {"unit": "TON", "quantity": "0", "value": "100.00"},
            False,
            {"quantity": ["Quantity must be 0.001 or more"]},
        ),
        (
            {"unit": "TON", "quantity": "1", "value": "not a number"},
            False,
            {"value": ["Total value must be a number, like 16.32"]},
        ),
        ({"unit": "TON", "quantity": "1", "value": "0"}, False, {"value": ["Total value must be 0.01 or more"]}),
        (
            {"unit": "TON", "quantity": "1", "value": "16.12345"},
            False,
            {"value": ["Total value must be less than 3 decimal places, like 123.45 or 156"]},
        ),
        (
            {"unit": "TON", "quantity": "1", "value": "16"},
            True,
            {},
        ),
        (
            {"unit": "TON", "quantity": "1.654", "value": "16"},
            True,
            {},
        ),
        (
            {"unit": "TON", "quantity": "1", "value": "16.32"},
            True,
            {},
        ),
        (
            {"unit": "NAR", "quantity": "1", "value": "16.32"},
            True,
            {},
        ),
        (
            {"unit": "NAR", "quantity": "1.4", "value": "16.32"},
            False,
            {"quantity": ["Items must be a whole number, like 16"]},
        ),
    ),
)
def test_product_unit_quantity_and_value_form_validation(data, is_valid, errors, request_with_session, get_units_mock):
    form = ProductUnitQuantityAndValueForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_onward_exported": ["Select yes if the product is going to any ultimate end-users"]},
        ),
        (
            {"is_onward_exported": True},
            True,
            {},
        ),
        (
            {"is_onward_exported": False},
            True,
            {},
        ),
    ),
)
def test_product_onward_exported_form_validation(data, is_valid, errors):
    form = ProductOnwardExportedForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "is_onward_altered_processed": [
                    "Select yes if the item will be altered or processed before it is exported again"
                ]
            },
        ),
        (
            {"is_onward_altered_processed": True},
            False,
            {"is_onward_altered_processed_comments": ["Enter how the product will be altered or processed"]},
        ),
        (
            {"is_onward_altered_processed": False},
            True,
            {},
        ),
        (
            {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "Onward altered"},
            True,
            {},
        ),
    ),
)
def test_product_onward_altered_processed_form_validation(data, is_valid, errors):
    form = ProductOnwardAlteredProcessedForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, cleaned_data",
    (
        (
            {"is_onward_altered_processed": False},
            {
                "is_onward_altered_processed": False,
                "is_onward_altered_processed_comments": "",
            },
        ),
    ),
)
def test_product_onward_altered_processed_form_cleaned_data(data, cleaned_data):
    form = ProductOnwardAlteredProcessedForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data == cleaned_data


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "is_onward_incorporated": [
                    "Select yes if the product will be incorporated into another item before it is onward exported"
                ]
            },
        ),
        (
            {"is_onward_incorporated": True},
            False,
            {"is_onward_incorporated_comments": ["Enter a description of what you are incorporating the product into"]},
        ),
        (
            {"is_onward_incorporated": False},
            True,
            {},
        ),
        (
            {"is_onward_incorporated": True, "is_onward_incorporated_comments": "Onward incorporated"},
            True,
            {},
        ),
    ),
)
def test_product_onward_incorporated_form_validation(data, is_valid, errors):
    form = ProductOnwardIncorporatedForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, cleaned_data",
    (
        (
            {"is_onward_incorporated": False},
            {
                "is_onward_incorporated": False,
                "is_onward_incorporated_comments": "",
            },
        ),
    ),
)
def test_product_onward_incorporated_form_cleaned_data(data, cleaned_data):
    form = ProductOnwardIncorporatedForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data == cleaned_data


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "uses_information_security": [
                    "Select yes if the product includes security features to protect information"
                ]
            },
        ),
        (
            {"uses_information_security": True},
            False,
            {"information_security_details": ["Enter details of the information security features"]},
        ),
        (
            {"uses_information_security": True, "information_security_details": ""},
            False,
            {"information_security_details": ["Enter details of the information security features"]},
        ),
        (
            {"uses_information_security": True, "information_security_details": "These are the details"},
            True,
            {},
        ),
        (
            {"uses_information_security": False},
            True,
            {},
        ),
    ),
)
def test_product_uses_information_security_form_validation(data, is_valid, errors):
    form = ProductUsesInformationSecurityForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_military_use": ["Select if the product is specially designed or modified for military use"]},
        ),
        (
            {"is_military_use": "yes_modified"},
            False,
            {"modified_military_use_details": ["Enter details of modifications"]},
        ),
        (
            {"is_military_use": "yes_modified", "modified_military_use_details": ""},
            False,
            {"modified_military_use_details": ["Enter details of modifications"]},
        ),
        (
            {"is_military_use": "yes_designed"},
            True,
            {},
        ),
        (
            {"is_military_use": "yes_modified", "modified_military_use_details": "Details"},
            True,
            {},
        ),
        (
            {"is_military_use": "no"},
            True,
            {},
        ),
    ),
)
def test_product_military_use_form_validation(data, is_valid, errors):
    form = ProductMilitaryUseForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"product_description": ["Enter a description of the product and what it is designed to do"]},
        ),
        (
            {"product_description": "Product description"},
            True,
            {},
        ),
    ),
)
def test_product_description_form_validation(data, is_valid, errors):
    form = ProductDescriptionForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
