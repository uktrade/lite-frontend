from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Submit

from django.urls import reverse_lazy

from core.common.forms import BaseForm
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
        title="Exhibition details",
        questions=[
            TextInput(title="Name", name="title"),
            DateInput(
                title="Exhibition start date",
                description="Exhibition start date",
                prefix="first_exhibition_date",
                name="first_exhibition_date",
            ),
            DateInput(
                title="Date the clearance is needed",
                description="For example, 12 11 2020",
                prefix="required_by_date",
                name="required_by_date",
            ),
            TextArea(
                title="The reason the clearance is needed by this date",
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
    # The minor edit flow has been disabled,
    # so all edits are major edits

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))


class ApplicationMajorEditConfirmationForm(BaseForm):
    class Layout:
        TITLE = "Are you sure you want to open your application for editing?"

    def __init__(self, *args, application_reference, cancel_url, **kwargs):
        self.application_reference = application_reference
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML.p(
                "Progress on the case will stop while you are making changes. The application will appear in 'Drafts' until you re-submit."
            ),
            HTML.p(
                """Submitting your edited application again will mean it is treated as a new case, with a new ECJU case reference.
                It will go back to the start of the assessment process to be re-checked by advisers."""
            ),
            HTML.p(f"Your own application reference '{self.application_reference}' will remain the same."),
        ]

    def get_layout_actions(self):
        return [
            Submit("submit", "Continue", data_module="disabling-button"),
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        ]


class ApplicationsListSortForm(BaseForm):
    class Layout:
        TITLE = ""

    CHOICES = [("submitted_at", "Date submitted"), ("updated_at", "Date updated")]

    sort_by = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select,
        label="Sort by",
        required=False,
    )

    def __init__(self, *args, action, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_method = "GET"
        self.helper.form_action = action

    def get_layout_fields(self):
        return [
            "sort_by",
        ]

    def get_layout_actions(self):
        return []
