from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML


def get_approval_advice_form_factory(advice):
    data = {
        "proviso": advice["proviso"],
        "approval_reasons": advice["text"],
        "instructions_to_exporter": advice["note"],
        "footnote_details": advice["footnote"],
    }

    return GiveApprovalAdviceForm(data=data)


def get_refusal_advice_form_factory(advice, denial_reasons_choices):
    data = {
        "refusal_reasons": advice["text"],
        "denial_reasons": [r for r in advice["denial_reasons"]],
    }

    return RefusalAdviceForm(data=data, denial_reasons=denial_reasons_choices)


class SelectAdviceForm(forms.Form):

    CHOICES = [("approve_all", "Approve all"), ("refuse_all", "Refuse all")]

    recommendation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))


class GiveApprovalAdviceForm(forms.Form):

    proviso = forms.CharField(
        label="Add a licence condition (optional)", widget=forms.Textarea(attrs={"rows": "10"}), required=False
    )
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="What are your reasons for approving?",
        error_messages={"required": "Enter a reason for approving"},
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to licence cover letter, subject to review by Licencing Unit.",
        required=False,
    )
    footnote_details = forms.CharField(
        label="Add a reporting footnote (optional)", widget=forms.Textarea(attrs={"rows": "5"}), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "proviso",
            "approval_reasons",
            "instructions_to_exporter",
            "footnote_details",
            HTML.details(
                "What is a footnote?",
                "Footnotes explain why products to a destination have been approved or refused. "
                "They will be publicly available in reports and data tables.",
            ),
            Submit("submit", "Submit"),
        )


class RefusalAdviceForm(forms.Form):
    def __init__(self, denial_reasons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(item["id"], item["id"]) for item in denial_reasons]
        self.fields["denial_reasons"] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple(),
            label='Select all <a href="/">refusal criteria</a> that apply',
        )
        self.fields["refusal_reasons"] = forms.CharField(
            label="What are your reasons for this refusal?",
            help_text='<a href="/">Choose a refusal reason from the template list</a>',
            widget=forms.Textarea(),
            error_messages={"required": "Enter a reason for refusing"},
        )
        self.helper = FormHelper()
        self.helper.layout = Layout("denial_reasons", "refusal_reasons", Submit("submit", "Submit"))


class DeleteAdviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("confirm", "Confirm"))
