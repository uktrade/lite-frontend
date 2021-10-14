from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML


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
