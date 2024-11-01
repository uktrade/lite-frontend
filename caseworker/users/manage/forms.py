from django import forms

from core.common.forms import BaseForm
from crispy_forms_gds.choices import Choice


class EditCaseworkerUser(BaseForm):
    class Layout:
        TITLE = "Edit"
        SUBMIT_BUTTON_TEXT = "Save and return"

    email = forms.EmailField(
        label="Email",
        error_messages={
            "required": "Enter an email address in the correct format, like name@example.com",
        },
    )

    role = forms.ChoiceField(
        label="Role",
    )

    team = forms.ChoiceField(
        label="Team",
    )

    queue = forms.ChoiceField(
        label="Default Queue",
    )

    def __init__(self, teams, *args, **kwargs):
        self.declared_fields["team"].choices = [Choice(t["id"], t["name"]) for t in teams]
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        # if email in self.organisation_users:
        #    raise forms.ValidationError("Enter an email address that is not registered to this organisation")
        return email

    def get_layout_fields(self):
        return (
            "email",
            "role",
            "team",
            "queue",
        )
