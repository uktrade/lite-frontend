import pytest

from caseworker.tau import forms


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        # Empty form
        ({}, False, ["report_summary", "goods", "does_not_have_control_list_entries"]),
        # Valid form
        ({"goods": ["test-id"], "report_summary": "test", "does_not_have_control_list_entries": True}, True, []),
        # Valid form - with comments
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "comments": "test",
            },
            True,
            [],
        ),
        # Invalid good-id
        (
            {"goods": ["test-id-not"], "report_summary": "test", "does_not_have_control_list_entries": True},
            False,
            ["goods"],
        ),
        # Missing goods
        ({"goods": [], "report_summary": "test", "does_not_have_control_list_entries": True}, False, ["goods"]),
        # Missing report-summart
        (
            {"goods": ["test-id"], "report_summary": None, "does_not_have_control_list_entries": True},
            False,
            ["report_summary"],
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {"goods": ["test-id"], "report_summary": "test", "does_not_have_control_list_entries": False},
            False,
            ["does_not_have_control_list_entries"],
        ),
        # does_not_have_control_list_entries=False but with control_list_entries
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
            },
            True,
            [],
        ),
        # Set is_wassenaar to False
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": False,
            },
            True,
            [],
        ),
        # Set is_wassenaar to False
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": True,
            },
            True,
            [],
        ),
    ),
)
def test_tau_assessment_form(data, valid, errors):
    form = forms.TAUAssessmentForm(
        goods={"test-id": "test-name"}, control_list_entries_choices=[("test-rating", "test-text")], data=data
    )
    assert form.is_valid() == valid
    assert list(form.errors.keys()) == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        # Empty form
        ({}, False, ["report_summary", "does_not_have_control_list_entries"]),
        # Valid form
        ({"report_summary": "test", "does_not_have_control_list_entries": True}, True, []),
        # Valid form - with comments
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "comments": "test",
            },
            True,
            [],
        ),
        # Missing report-summart
        (
            {"report_summary": None, "does_not_have_control_list_entries": True},
            False,
            ["report_summary"],
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {"report_summary": "test", "does_not_have_control_list_entries": False},
            False,
            ["does_not_have_control_list_entries"],
        ),
        # does_not_have_control_list_entries=False but with control_list_entries
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
            },
            True,
            [],
        ),
        # Set is_wassenaar to False
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": False,
            },
            True,
            [],
        ),
        # Set is_wassenaar to True
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": True,
            },
            True,
            [],
        ),
    ),
)
def test_tau_assessment_form(data, valid, errors):
    form = forms.TAUEditForm(control_list_entries_choices=[("test-rating", "test-text")], data=data)
    assert form.is_valid() == valid
    assert list(form.errors.keys()) == errors
