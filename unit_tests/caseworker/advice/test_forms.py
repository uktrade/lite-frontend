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
