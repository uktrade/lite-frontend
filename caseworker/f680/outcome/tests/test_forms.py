import pytest

from freezegun import freeze_time

from caseworker.f680.outcome.forms import SelectOutcomeForm, ApproveOutcomeForm, RefuseOutcomeForm


@freeze_time("2025-04-14")
@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "security_release_requests": ["This field is required."],
                "outcome": ["Select if you approve or refuse"],
                "validity_start_date": ["Enter the validity start date"],
                "validity_end_date": ["Enter the validity end date"],
            },
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
            },
            False,
            {
                "outcome": ["Select if you approve or refuse"],
                "validity_start_date": ["Enter the validity start date"],
                "validity_end_date": ["Enter the validity end date"],
            },
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "outcome": "approve",
            },
            False,
            {
                "validity_start_date": ["Enter the validity start date"],
                "validity_end_date": ["Enter the validity end date"],
            },
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "outcome": "approve",
                "validity_start_date_0": "01",
                "validity_start_date_1": "05",
                "validity_start_date_2": "2024",
                "validity_end_date_0": "01",
                "validity_end_date_1": "05",
                "validity_end_date_2": "2026",
            },
            False,
            {"validity_start_date": ["Validity start date must be from today or in the future"]},
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "outcome": "approve",
                "validity_start_date_0": "14",
                "validity_start_date_1": "04",
                "validity_start_date_2": "2025",
                "validity_end_date_0": "14",
                "validity_end_date_1": "04",
                "validity_end_date_2": "2027",
            },
            True,
            {},
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "outcome": "approve",
                "validity_start_date_0": "14",
                "validity_start_date_1": "04",
                "validity_start_date_2": "2025",
                "validity_end_date_0": "14",
                "validity_end_date_1": "01",
                "validity_end_date_2": "2027",
            },
            False,
            {"validity_end_date": ["Outcome validity is less than 2 years"]},
        ),
        (
            {
                "security_release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "outcome": "approve",
                "validity_start_date_0": "14",
                "validity_start_date_1": "04",
                "validity_start_date_2": "2025",
                "validity_end_date_0": "14",
                "validity_end_date_1": "01",
                "validity_end_date_2": "2028",
            },
            False,
            {"validity_end_date": ["Validity end date must be within 2 years"]},
        ),
    ),
)
def test_select_outcome_form_valid(data, valid_status, errors):
    release_requests = [
        {
            "id": "123465e5-4c80-4d0a-aef5-db94908b0417",
            "security_grading": {"key": "official", "value": "Official"},
            "recipient": {
                "name": "Test entity",
                "country": {
                    "name": "Australia",
                },
            },
        }
    ]
    form = SelectOutcomeForm(data=data, security_release_requests=release_requests)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "security_grading": ["Select the security release"],
                "approval_types": ["Select approval types"],
            },
        ),
        (
            {
                "security_grading": "official",
                "conditions": "",
            },
            False,
            {
                "approval_types": ["Select approval types"],
            },
        ),
        (
            {
                "security_grading": "official",
                "approval_types": ["initial_discussion_or_promoting", "demonstration_overseas"],
            },
            True,
            {},
        ),
    ),
)
def test_approve_outcome_form_valid(data, valid_status, errors):
    all_approval_types = ["initial_discussion_or_promoting", "demonstration_overseas", "training", "supply"]
    form = ApproveOutcomeForm(data=data, all_approval_types=all_approval_types)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "refusal_reasons": ["Enter refusal reasons"],
            },
        ),
        (
            {
                "refusal_reasons": "Doesn't meet criteria",
            },
            True,
            {},
        ),
    ),
)
def test_refuse_outcome_form_valid(data, valid_status, errors):
    form = RefuseOutcomeForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors
