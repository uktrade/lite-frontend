import pytest

from caseworker.advice.forms.approval import SelectAdviceForm
from caseworker.advice.forms.consolidate import ConsolidateSelectAdviceForm
from caseworker.advice.forms.countersign import CountersignAdviceForm, CountersignDecisionAdviceForm
from caseworker.advice.forms.forms import GiveApprovalAdviceForm, FCDOApprovalAdviceForm


@pytest.mark.parametrize(
    "data, valid_status",
    (
        ({"approval_reasons": "meets the requirements", "instructions_to_exporter": "no specific instructions"}, True),
        ({"instructions_to_exporter": "no specific instructions"}, False),
    ),
)
def test_give_approval_advice_form_valid(data, valid_status):
    form = GiveApprovalAdviceForm(
        data=data, approval_reason={"results": []}, proviso={"results": []}, footnote_details={"results": []}
    )
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors["approval_reasons"] == ["Enter a reason for approving"]


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
    form = SelectAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors["recommendation"] == ["Select if you approve all or refuse all"]


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
    form = ConsolidateSelectAdviceForm(team_name=None, data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors["recommendation"] == ["Select if you approve or refuse"]


@pytest.mark.parametrize(
    "team_name, label",
    (
        (None, "What is the combined recommendation?"),
        ("team name", "What is the combined recommendation for team name?"),
    ),
)
def test_consolidate_select_advice_form_recommendation_label(team_name, label):
    form = ConsolidateSelectAdviceForm(team_name=team_name)
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
    form = CountersignAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors["approval_reasons"] == ["Enter why you agree with the recommendation"]


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        ({"outcome_accepted": True, "approval_reasons": "approved", "rejected_reasons": ""}, True, {}),
        ({"outcome_accepted": False, "approval_reasons": "", "rejected_reasons": "rejected"}, True, {}),
        (
            {"outcome_accepted": "", "approval_reasons": "approved", "rejected_reasons": ""},
            False,
            {"outcome_accepted": ["Select yes if you agree with the recommendation"]},
        ),
        (
            {"outcome_accepted": True, "approval_reasons": "", "rejected_reasons": ""},
            False,
            {"approval_reasons": ["Enter a reason for countersigning"]},
        ),
        (
            {"outcome_accepted": False, "approval_reasons": "", "rejected_reasons": ""},
            False,
            {"rejected_reasons": ["Enter a message explaining why the case is being returned"]},
        ),
        ({}, False, {"outcome_accepted": ["Select yes if you agree with the recommendation"]}),
    ),
)
def test_countersign_decision_advice_form_valid(data, valid_status, errors):
    form = CountersignDecisionAdviceForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


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
def test_give_fcdo_approval_advice_form_valid(data, valid_status):
    form = FCDOApprovalAdviceForm(
        data=data,
        countries={"GB": "United Kingdom"},
        approval_reason={"results": []},
        proviso={"results": []},
        footnote_details={"results": []},
    )
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors["countries"] == ["Select the destinations you want to make recommendations for"]
