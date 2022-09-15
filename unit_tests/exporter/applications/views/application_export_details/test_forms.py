import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.applications.views.application_export_details.forms import (
    SecurityClassifiedDetailsForm,
    F680ReferenceNumberForm,
    SecurityOtherDetailsForm,
    F1686DetailsForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_security_classified": ["Select yes if product's are security required"]},
        ),
        (
            {"is_security_classified": True},
            False,
            {"mod_security_classified_approvals": ["Select at least 1 security approval"]},
        ),
        (
            {"is_security_classified": False},
            True,
            {},
        ),
        (
            {"is_security_classified": True, "mod_security_classified_approvals": ["F680"]},
            True,
            {},
        ),
    ),
)
def test_security_classified_details(data, is_valid, errors):
    form = SecurityClassifiedDetailsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"f680_reference_number": ["Enter a reference number"]},
        ),
        (
            {"f680_reference_number": "dummy ref"},
            True,
            {},
        ),
    ),
)
def test_f680_reference_number(data, is_valid, errors):
    form = F680ReferenceNumberForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"mod_security_other_details": ["Enter approval details"]},
        ),
        (
            {"mod_security_other_details": "dummy other details"},
            True,
            {},
        ),
    ),
)
def test_security_other_details(data, is_valid, errors):
    form = SecurityOtherDetailsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, file, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "f1686_contracting_authority": ["Enter a contracting authority"],
                "is_approval_document_available": ["Select if you have an approval document"],
            },
        ),
        (
            {"f1686_contracting_authority": "signed by the joe"},
            {},
            False,
            {
                "is_approval_document_available": ["Select if you have an approval document"],
            },
        ),
        (
            {"is_approval_document_available": True, "f1686_contracting_authority": "signed by the joe"},
            {},
            False,
            {
                "f1686_approval_document": ["Select an approval document"],
            },
        ),
        (
            {"is_approval_document_available": True, "f1686_contracting_authority": "signed by the joe"},
            {"f1686_approval_document": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
        (
            {"is_approval_document_available": False, "f1686_contracting_authority": "signed by the joe"},
            {},
            False,
            {
                "f1686_approval_date": ["Enter the approval date"],
                "f1686_reference_number": ["Enter a reference number"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
            },
            {},
            False,
            {
                "f1686_approval_date": ["Enter the approval date"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "20",
            },
            {},
            False,
            {
                "f1686_approval_date": ["Approval date must include a month", "Approval date must include a year"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "20",
                "f1686_approval_date_2": "2020",
            },
            {},
            False,
            {
                "f1686_approval_date": ["Approval date must include a month"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "20",
                "f1686_approval_date_1": "2",
                "f1686_approval_date_2": "2040",
            },
            {},
            False,
            {
                "f1686_approval_date": ["Approval date must be in the past"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "30",
                "f1686_approval_date_1": "32",
                "f1686_approval_date_2": "2020",
            },
            {},
            False,
            {
                "f1686_approval_date": ["Approval date must be a real date"],
            },
        ),
        (
            {
                "is_approval_document_available": False,
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "02",
                "f1686_approval_date_1": "02",
                "f1686_approval_date_2": "2020",
            },
            {},
            True,
            {},
        ),
    ),
)
def test_f1686_details(data, file, is_valid, errors):
    form = F1686DetailsForm(data=data, files=file)
    assert form.is_valid() == is_valid
    assert form.errors == errors
