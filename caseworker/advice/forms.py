from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Size, Submit, HTML


class GiveApprovalAdviceForm(forms.Form):

    proviso = forms.CharField(label="Add a licence condition (optional)", widget=forms.Textarea, required=False)
    approval_reasons = forms.CharField(
        widget=forms.Textarea,
        label="What are your reasons for approving?",
        error_messages={"required": "Enter a reason for approving"},
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea,
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to licence cover letter, subject to review by Licencing Unit.",
        required=False,
    )
    footnote_details = forms.CharField(
        label="Add a reporting footnote (optional)", widget=forms.Textarea, required=False
    )

    def __init__(self, queue_pk, pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field.textarea("proviso", rows=10,),
            Field.textarea("approval_reasons", rows=10,),
            Field.textarea("instructions_to_exporter", rows=10,),
            Field.textarea("footnote_details", rows=5,),
            HTML.details(
                "What is a footnote?",
                "Footnotes explain why products to a destination have been approved or refused. "
                "They will be publicly available in reports and data tables.",
            ),
            Submit("submit", "Submit"),
        )
