from django import forms

from core.common.forms import BaseForm
from crispy_forms_gds.layout import HTML


class ChangeLicenceStatusForm(BaseForm):
    class Layout:
        TITLE = "Change licence status"
        SUBMIT_BUTTON_TEXT = "Continue"

    status = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        label="Select a licence status to change",
        error_messages={"required": "Select a status to change the licence to"},
    )

    def get_layout_fields(self):
        self.fields["status"].choices += self.statuses

        p_text = HTML.p(
            f"You should only alter the licence status of  {self.reference_code} "
            "if you have documented the reasons why in the case notes and timeline."
        )

        return (
            p_text,
            "status",
        )

    def __init__(self, *args, statuses, reference_code, cancel_url, **kwargs):

        self.cancel_url = cancel_url
        self.statuses = statuses
        self.reference_code = reference_code

        super().__init__(*args, **kwargs)

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )

        return layout_actions


class ChangeLicenceStatusConfirmationForm(BaseForm):
    class Layout:
        TITLE = "Are you sure you want to alter the status of the licence?"
        SUBMIT_BUTTON_TEXT = "Continue"

    def __init__(self, *args, cancel_url, **kwargs):
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return (
            HTML.p(
                "if you change it to "
                "Revoked"
                "  or Suspended  the exporter cannot export the products and any attempt to do so will be viewed as an offence."
            ),
        )

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )
        return layout_actions
