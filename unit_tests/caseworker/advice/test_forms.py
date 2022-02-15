import pytest

from caseworker.advice import forms


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"approval_reasons": "meets the requirements", "instructions_to_exporter": "no specific instructions"}, True),
        ({"instructions_to_exporter": "no specific instructions"}, False),
    ),
)
def test_give_approval_advice_form_valid(data, valid_status):
    form = forms.GiveApprovalAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if valid_status == False:
        assert form.errors["approval_reasons"][0] == "Enter a reason for approving"


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"recommendation": "approve_all"}, True),
        ({"recommendation": "refuse_all"}, True),
        ({"recommendation": None}, False),
        ({}, False),
    ),
)
def test_select_advice_form_valid(data, valid_status):
    form = forms.SelectAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert "recommendation" in form.errors.keys()
        assert "Select if you approve all or refuse all" in form.errors["recommendation"]


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"recommendation": "approve"}, True),
        ({"recommendation": "refuse"}, True),
        ({"recommendation": None}, False),
        ({}, False),
    ),
)
def test_consolidate_select_advice_form_valid(data, valid_status):
    form = forms.ConsolidateSelectAdviceForm(team_name=None, data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert "recommendation" in form.errors.keys()
        assert "Select if you approve or refuse" in form.errors["recommendation"]


@pytest.mark.parametrize(
    "team_name, label",
    (
        (None, "What is the combined recommendation?"),
        ("team name", "What is the combined recommendation for team name?"),
    ),
)
def test_consolidate_select_advice_form_recommendation_label(team_name, label):
    form = forms.ConsolidateSelectAdviceForm(team_name=team_name)
    assert form.fields["recommendation"].label == label


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"approval_reasons": "some reason"}, True),
        ({"approval_reasons": None}, False),
        ({}, False),
    ),
)
def test_countersign_advice_form_valid(data, valid_status):
    form = forms.CountersignAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert "approval_reasons" in form.errors.keys()
        assert "Enter why you agree with the recommendation" in form.errors["approval_reasons"]


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"approval_reasons": "meets the requirements", "countries": ["GB"]}, True),
        (
            {
                "approval_reasons": "meets the requirements",
                "instructions_to_exporter": "no specific instructions",
                "countries": ["GB"],
            },
            True,
        ),
        ({"approval_reasons": "meets the requirements"}, False),
    ),
)
def test_give_approval_advice_form_valid(data, valid_status):
    form = forms.FCDOApprovalAdviceForm(data=data, countries={"GB": "United Kingdom"})
    form.is_valid()
    assert form.is_valid() == valid_status
    if valid_status == False:
        assert "Select the destinations you want to make recommendations for" in form.errors["countries"][0]
