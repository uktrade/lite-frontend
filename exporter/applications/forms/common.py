from django import forms
from django.forms.widgets import HiddenInput

from django.urls import reverse_lazy

from exporter.applications.forms.edit import told_by_an_official_form, reference_name_form
from exporter.core.constants import STANDARD
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import (
    HiddenField,
    Form,
    BackLink,
    TextArea,
    Option,
    FormGroup,
    TextInput,
    DateInput,
    Label,
    Checkboxes,
)
from lite_forms.helpers import conditional
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit


def application_copy_form(application_type=None):
    return FormGroup(
        forms=[
            reference_name_form(),
            conditional((application_type == STANDARD), told_by_an_official_form()),
        ]
    )


def exhibition_details_form(application_id):
    return Form(
        title=strings.Exhibition.EXHIBITION_TITLE,
        questions=[
            TextInput(title=strings.Exhibition.TITLE, name="title"),
            DateInput(
                title=strings.Exhibition.FIRST_EXHIBITION_DATE,
                description=strings.Exhibition.DATE_DESCRIPTION,
                prefix="first_exhibition_date",
                name="first_exhibition_date",
            ),
            DateInput(
                title=strings.Exhibition.REQUIRED_BY_DATE,
                description=strings.Exhibition.DATE_DESCRIPTION,
                prefix="required_by_date",
                name="required_by_date",
            ),
            TextArea(
                title=strings.Exhibition.REASON_FOR_CLEARANCE,
                name="reason_for_clearance",
                optional=True,
                extras={"max_length": 2000},
            ),
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION,
            reverse_lazy("applications:task_list", kwargs={"pk": application_id}),
        ),
    )


def declaration_form(application_id):
    return Form(
        title=strings.declaration.Declaration.TITLE,
        questions=[
            HiddenField(name="submit_declaration", value=True),
            Label(strings.declaration.Declaration.PARAGRAPH_ONE),
            Label(strings.declaration.Declaration.PARAGRAPH_TWO),
            Label(strings.declaration.Declaration.PARAGRAPH_THREE),
            Label(strings.declaration.Declaration.PARAGRAPH_FOUR),
            Checkboxes(
                name="agreed_to_foi",
                options=[
                    Option(
                        key="True",
                        value=strings.declaration.FOI.INFORMATION_DISCLOSURE_TITLE,
                    ),
                ],
                classes=["govuk-checkboxes--small"],
            ),
            TextArea(
                title=strings.declaration.FOI.INFORMATION_DISCLOSURE_DETAILS,
                name="foi_reason",
            ),
            Label(strings.declaration.Declaration.FOI_MORE_ADVICE),
            Label(strings.declaration.Declaration.FOI_GUIDANCE),
            TextInput(
                title="Confirm that you agree to the above by typing 'I AGREE' in this box",
                name="agreed_to_declaration_text",
            ),
            Label(
                """Please note, your application must be checked thoroughly and only say 'I agree' if you are content
                that the ELA is accurate. It may not be possible to make changes to the application after
                it has been submitted and if so, you may have to reapply."""
            ),
        ],
        default_button_name=strings.declaration.Declaration.BUTTON_TITLE,
        back_link=BackLink(
            strings.declaration.Declaration.BACK,
            reverse_lazy("applications:summary", kwargs={"pk": application_id}),
        ),
        javascript_imports={"/javascripts/declaration.js"},
    )


class EditApplicationForm(forms.Form):
    # CHOICES = [
    #     ("minor", "Delete a product, third party or country"),
    #     ("major", "Add a product or edit something else"),
    # ]
    # edit_type = forms.ChoiceField(
    #     choices=CHOICES,
    #     widget=forms.RadioSelect,
    #     label="",
    #     error_messages={
    #         "required": "Please select an option to proceed.",
    #     },
    # )
    # The minor edit flow has been temporarily disabled
    edit_type = forms.CharField(widget=HiddenInput, initial="major")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
