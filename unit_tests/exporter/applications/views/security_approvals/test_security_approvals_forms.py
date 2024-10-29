import pytest

from exporter.applications.views.security_approvals.forms import (
    SecurityClassifiedDetailsForm,
    F680ReferenceNumberForm,
    SecurityOtherDetailsForm,
    F1686DetailsForm,
    SubjectToITARControlsForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_mod_security_approved": ["Select no if you do not have an MOD security approval"]},
        ),
        (
            {"is_mod_security_approved": True},
            False,
            {"security_approvals": ["Select the type of security approval"]},
        ),
        (
            {"is_mod_security_approved": False},
            True,
            {},
        ),
        (
            {"is_mod_security_approved": True, "security_approvals": ["F680"]},
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
            {"subject_to_itar_controls": ["Select no if the products are not subject to ITAR controls"]},
        ),
        (
            {"subject_to_itar_controls": True},
            True,
            {},
        ),
        (
            {"subject_to_itar_controls": False},
            True,
            {},
        ),
    ),
)
def test_subject_to_itar_controls(data, is_valid, errors):
    form = SubjectToITARControlsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"f680_reference_number": [" Enter the F680 reference number"]},
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
            {"other_security_approval_details": ["Enter the details of your written approval"]},
        ),
        (
            {"other_security_approval_details": "dummy other details"},
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
                "f1686_contracting_authority": ["Enter the contracting authority (or signatory and job role)"],
                "f1686_approval_date": ["Enter the approval date"],
            },
        ),
        (
            {
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
