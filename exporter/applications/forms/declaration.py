from django import forms

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm
from core.forms.layouts import (
    ConditionalRadiosQuestion,
    ConditionalRadios,
)


class ApplicationDeclarationForm(BaseForm):
    class Layout:
        TITLE = "Submit your application"
        BACK_LINK_TEXT = "Back to check your answers"
        HEADING_FOI_DISCLOSURE = "Freedom of Information disclosure"
        HEADING_DECLARATION = "Declaration"
        SUBMIT_BUTTON_TEXT = "Accept and submit"

    # TODO: we should update lite-api so that Yes is True and No is False
    agreed_to_foi = forms.ChoiceField(
        choices=((False, "Yes"), (True, "No")),
        widget=forms.RadioSelect,
        label="",
        help_text="",
    )

    foi_reason = forms.CharField(
        widget=forms.Textarea,
        label="Explain why the disclosure of information would be harmful to your interests. While the Export Control Joint Unit (ECJU) will take your views into account, they cannot guarantee that the information will not be made public.",
        error_messages={"required": "Explain why the disclosure of information would be harmful to your interests"},
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML(f'<h2 class="govuk-heading-m">{self.Layout.HEADING_FOI_DISCLOSURE}</h2>'),
            HTML.p(
                "Any information you provide in this application may be made public under the Freedom of Information Act 2000."
            ),
            HTML.p("Do you agree to make the application details publicly available?"),
            ConditionalRadios("agreed_to_foi", "Yes", ConditionalRadiosQuestion("No", "foi_reason")),
            HTML(
                '<p class="govuk-body"><a class="govuk-link" href="https://ico.org.uk/for-organisations/guide-to-freedom-of-information/">Find out more about the Freedom of Information Act 2000 and exemptions at the Information Commissioner\'s Office</a>.</p>'
            ),
            HTML(f'<h2 class="govuk-heading-m">{self.Layout.HEADING_DECLARATION}</h2>'),
            HTML(
                f'<p class="govuk-body">Making a misleading application is an offence as set out in the <a class="govuk-link" href="https://www.legislation.gov.uk/uksi/2008/3231/contents/made">Export Control Order 2008</a>.</p>'
            ),
            HTML.p(
                "The licensee must comply with the licence conditions even, where relevant, after completing the activity authorised by the licence. Failure to do so is an offence."
            ),
            HTML.p(
                "Information provided in this application may be passed to international organisations or other governments in accordance with commitments entered into by His Majesty's Government."
            ),
            HTML.p(
                "If ECJU staff have completed this application on your behalf, they based it on the information you provided. You as the exporter are responsible for the accuracy of the information."
            ),
        ]
