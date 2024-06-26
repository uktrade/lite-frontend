from django import forms
from django.forms.widgets import HiddenInput

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit

from django.urls import reverse_lazy

from exporter.applications.forms.edit import told_by_an_official_form, reference_name_form
from exporter.core.constants import STANDARD
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import (
    Form,
    BackLink,
    TextArea,
    FormGroup,
    TextInput,
    DateInput,
)
from lite_forms.helpers import conditional


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
    edit_type = forms.CharField(widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
