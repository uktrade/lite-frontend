import datetime
import pytest
import requests
import uuid

from dateutil.relativedelta import relativedelta
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmIsDeactivatedForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmQuantityAndValueForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
    FirearmSerialIdentificationMarkingsForm,
    FirearmMadeBefore1938Form,
    FirearmYearOfManufactureForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"category": ['Select a firearm category, or select "None of the above"']}),
        (
            {"category": ["NON_AUTOMATIC_SHOTGUN", "NONE"]},
            False,
            {"category": ['Select a firearm category, or select "None of the above"']},
        ),
        ({"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_RIFLE"]}, True, {}),
        ({"category": ["NONE"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


def test_firearm_product_control_list_entry_form_init_control_list_entries(request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(request=request_with_session)
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
def test_firearm_product_control_list_entry_form(data, is_valid, errors, request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(data=data, request=request_with_session)
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
def test_firearm_pv_security_gradings_form(data, is_valid, errors):
    form = FirearmPvGradingForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


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
def test_firearm_pv_security_grading_details_form(data, is_valid, errors, request_with_session, pv_gradings):
    form = FirearmPvGradingDetailsForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"calibre": ["Enter the calibre"]}),
        ({"calibre": "calibre 123"}, True, {}),
    ),
)
def test_firearm_calibre_form(data, is_valid, errors):
    form = FirearmCalibreForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_replica": ["Select yes if the product is a replica firearm"]}),
        ({"is_replica": True}, False, {"replica_description": ["Enter a description"]}),
        ({"is_replica": True, "replica_description": "Replica description"}, True, {}),
        ({"is_replica": False}, True, {}),
    ),
)
def test_firearm_replica_form(data, is_valid, errors):
    form = FirearmReplicaForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_rfd_certificate_valid": ["Select yes if your registered firearms dealer certificate is still valid"]},
        ),
        ({"is_rfd_certificate_valid": True}, True, {}),
    ),
)
def test_firearm_validity_form(data, is_valid, errors):
    rfd_certificate = {
        "id": uuid.uuid4(),
        "document": {
            "name": "TEST DOCUMENT",
        },
    }

    form = FirearmRFDValidityForm(data=data, rfd_certificate=rfd_certificate)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_registered_firearm_dealer": ["Select yes if you are a registered firearms dealer"]}),
        ({"is_registered_firearm_dealer": True}, True, {}),
    ),
)
def test_firearm_registered_firearms_dealer_form(data, is_valid, errors):
    form = FirearmRegisteredFirearmsDealerForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Enter the expiry date"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today() - datetime.timedelta(days=10)),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today()),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today() + relativedelta(years=5, days=1)),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be within 5 years"],
            },
        ),
        (
            {"expiry_date_1": "12", "expiry_date_2": "2022"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a day"],
            },
        ),
        (
            {"expiry_date_0": "1", "expiry_date_2": "2022"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a month"],
            },
        ),
        (
            {"expiry_date_0": "1", "expiry_date_1": "12"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a year"],
            },
        ),
        (
            {"expiry_date_0": "abc", "expiry_date_1": "abc", "expiry_date_2": "abc"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be a real date"],
            },
        ),
        (
            {
                "reference_code": "abcdef",
                **decompose_date(
                    "expiry_date",
                    datetime.date.today() + datetime.timedelta(days=1),
                ),
            },
            {"file": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
    ),
)
def test_firearm_attach_rfd_certificate_form(data, files, is_valid, errors):
    form = FirearmAttachRFDCertificate(data=data, files=files)
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
    form = FirearmDocumentAvailability(data=data)
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
    form = FirearmDocumentSensitivityForm(data=data)
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
    form = FirearmDocumentUploadForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"firearms_act_section": ["Select which section of the Firearms Act 1968 the is product covered by"]},
        ),
        (
            {"firearms_act_section": "firearms_act_section1"},
            True,
            {},
        ),
        (
            {"firearms_act_section": "dont_know"},
            False,
            {"not_covered_explanation": ["Explain why you don't know"]},
        ),
    ),
)
def test_firearm_firearm_act_1968_form(data, is_valid, errors):
    form = FirearmFirearmAct1968Form(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "file": ["Select a firearm certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Enter the expiry date"],
            },
        ),
        (
            decompose_date("section_certificate_date_of_expiry", datetime.date.today() - datetime.timedelta(days=10)),
            {},
            False,
            {
                "file": ["Select a firearm certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date(
                "section_certificate_date_of_expiry", datetime.date.today() + relativedelta(years=5, days=1)
            ),
            {},
            False,
            {
                "file": ["Select a firearm certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be within 5 years"],
            },
        ),
        (
            {
                "section_certificate_number": "abcdef",
                **decompose_date(
                    "section_certificate_date_of_expiry",
                    datetime.date.today() + datetime.timedelta(days=1),
                ),
            },
            {"file": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
        (
            {
                "section_certificate_missing": True,
            },
            {},
            False,
            {
                "section_certificate_missing_reason": ["Enter a reason why you do not have a firearm certificate"],
            },
        ),
    ),
)
def test_firearm_attach_firearm_certificate_form(data, files, is_valid, errors):
    form = FirearmAttachFirearmCertificateForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "file": ["Select a shotgun certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Enter the expiry date"],
            },
        ),
        (
            decompose_date("section_certificate_date_of_expiry", datetime.date.today() - datetime.timedelta(days=10)),
            {},
            False,
            {
                "file": ["Select a shotgun certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date(
                "section_certificate_date_of_expiry", datetime.date.today() + relativedelta(years=5, days=1)
            ),
            {},
            False,
            {
                "file": ["Select a shotgun certificate"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be within 5 years"],
            },
        ),
        (
            {
                "section_certificate_number": "abcdef",
                **decompose_date(
                    "section_certificate_date_of_expiry",
                    datetime.date.today() + datetime.timedelta(days=1),
                ),
            },
            {"file": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
        (
            {
                "section_certificate_missing": True,
            },
            {},
            False,
            {
                "section_certificate_missing_reason": ["Enter a reason why you do not have a shotgun certificate"],
            },
        ),
    ),
)
def test_firearm_attach_shotgun_certificate_form(data, files, is_valid, errors):
    form = FirearmAttachShotgunCertificateForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "file": ["Select a section 5 letter of authority"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Enter the expiry date"],
            },
        ),
        (
            decompose_date("section_certificate_date_of_expiry", datetime.date.today() - datetime.timedelta(days=10)),
            {},
            False,
            {
                "file": ["Select a section 5 letter of authority"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date(
                "section_certificate_date_of_expiry", datetime.date.today() + relativedelta(years=5, days=1)
            ),
            {},
            False,
            {
                "file": ["Select a section 5 letter of authority"],
                "section_certificate_number": ["Enter the certificate number"],
                "section_certificate_date_of_expiry": ["Expiry date must be within 5 years"],
            },
        ),
        (
            {
                "section_certificate_number": "abcdef",
                **decompose_date(
                    "section_certificate_date_of_expiry",
                    datetime.date.today() + datetime.timedelta(days=1),
                ),
            },
            {"file": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
        (
            {
                "section_certificate_missing": True,
            },
            {},
            False,
            {
                "section_certificate_missing_reason": [
                    "Enter a reason why you do not have a section 5 letter of authority"
                ],
            },
        ),
    ),
)
def test_firearm_attach_section_5_letter_of_authority_form(data, files, is_valid, errors):
    form = FirearmAttachSection5LetterOfAuthorityForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "is_covered_by_section_5": [
                    "Select whether the product is covered by section 5 of the Firearms Act 1968"
                ]
            },
        ),
        (
            {
                "is_covered_by_section_5": "dont_know",
            },
            True,
            {},
        ),
        (
            {
                "is_covered_by_section_5": "dont_know",
            },
            True,
            {},
        ),
        (
            {
                "is_covered_by_section_5": "yes",
            },
            True,
            {},
        ),
        (
            {
                "is_covered_by_section_5": "no",
            },
            True,
            {},
        ),
    ),
)
def test_firearm_section_5_form(data, is_valid, errors):
    form = FirearmSection5Form(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_made_before_1938": ["Select yes if the product was made before 1938"]}),
        ({"is_made_before_1938": True}, True, {}),
        ({"is_made_before_1938": False}, True, {}),
    ),
)
def test_firearm_made_before_1938_form(data, is_valid, errors):
    form = FirearmMadeBefore1938Form(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"year_of_manufacture": ["Enter the year it was made"]}),
        ({"year_of_manufacture": 2022}, False, {"year_of_manufacture": ["The year must be before 1938"]}),
        ({"year_of_manufacture": 1938}, False, {"year_of_manufacture": ["The year must be before 1938"]}),
        ({"year_of_manufacture": 999}, False, {"year_of_manufacture": ["The year it was made must be a real year"]}),
        ({"year_of_manufacture": 1}, False, {"year_of_manufacture": ["The year it was made must be a real year"]}),
        ({"year_of_manufacture": "-1"}, False, {"year_of_manufacture": ["The year it was made must be a real year"]}),
        ({"year_of_manufacture": 1937}, True, {}),
    ),
)
def test_firearm_year_of_manufacture_form(data, is_valid, errors):
    form = FirearmYearOfManufactureForm(data=data)
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
def test_firearm_quantity_and_value(data, is_valid, errors):
    form = FirearmQuantityAndValueForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (({}, False, {"is_deactivated": ["Select yes if the product has been deactivated"]}),),
)
def test_firearm_is_deactivated_form(data, is_valid, errors):
    form = FirearmIsDeactivatedForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "date_of_deactivation": ["Enter the deactivation date"],
                "is_deactivated_to_standard": [
                    "Select yes if the product has been deactivated to UK proof house standards"
                ],
                "not_deactivated_to_standard_comments": [
                    "Enter who deactivated the product and to what standard it was done"
                ],
            },
        ),
    ),
)
def test_firearm_deactivation_details_form(data, is_valid, errors):
    form = FirearmDeactivationDetailsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"serial_numbers_available": ["Select if each product will have a serial number"]},
        ),
        (
            {
                "serial_numbers_available": "NOT_AVAILABLE",
            },
            False,
            {"no_identification_markings_details": ["Enter why products will not have serial numbers"]},
        ),
        (
            {
                "serial_numbers_available": "AVAILABLE",
            },
            True,
            {},
        ),
        (
            {
                "serial_numbers_available": "LATER",
            },
            True,
            {},
        ),
        (
            {
                "serial_numbers_available": "NOT_AVAILABLE",
                "no_identification_markings_details": "no markings",
            },
            True,
            {},
        ),
    ),
)
def test_firearm_identificateion_markings_form(data, is_valid, errors):
    form = FirearmSerialIdentificationMarkingsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
