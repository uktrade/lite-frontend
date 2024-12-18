from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout

from core.forms.layouts import (
    ConditionalRadios,
    ConditionalRadiosQuestion,
)
from core.forms.utils import coerce_str_to_bool


class CountersignAdviceForm(forms.Form):
    DOCUMENT_TITLE = "Review and countersign this case"
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Explain why you are agreeing with this recommendation",
        error_messages={"required": "Enter why you agree with the recommendation"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout("approval_reasons")


class CountersignDecisionAdviceForm(forms.Form):
    DECISION_CHOICES = [(True, "Yes"), (False, "No")]

    outcome_accepted = forms.TypedChoiceField(
        choices=DECISION_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        label="Do you agree with this recommendation?",
        error_messages={"required": "Select yes if you agree with the recommendation"},
    )
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Explain your reasons",
        required=False,
    )
    rejected_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Message to the case officer (explaining why the case is being returned)",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            ConditionalRadios(
                "outcome_accepted",
                ConditionalRadiosQuestion("Yes", Field("approval_reasons")),
                ConditionalRadiosQuestion("No", Field("rejected_reasons")),
            ),
        )

    def clean_approval_reasons(self):
        outcome_accepted = self.cleaned_data.get("outcome_accepted")
        approval_reasons = self.cleaned_data.get("approval_reasons")
        if outcome_accepted and not self.cleaned_data.get("approval_reasons"):
            self.add_error("approval_reasons", "Enter a reason for countersigning")

        return approval_reasons

    def clean_rejected_reasons(self):
        outcome_accepted = self.cleaned_data.get("outcome_accepted")
        rejected_reasons = self.cleaned_data.get("rejected_reasons")
        if outcome_accepted is False and not self.cleaned_data.get("rejected_reasons"):
            self.add_error("rejected_reasons", "Enter a message explaining why the case is being returned")

        return rejected_reasons
