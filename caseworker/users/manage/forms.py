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
        widget=forms.Select(attrs={"id": "role", "data-attribute": "1234"}),
    )

    team = forms.ChoiceField(label="Team", widget=forms.Select(attrs={"id": "team"}))

    default_queue = forms.ChoiceField(label="Default Queue", widget=forms.Select(attrs={"id": "default_queue"}))

    def __init__(self, teams, roles, queues, can_caseworker_edit_role, can_caseworker_edit_team, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].widget.attrs["disabled"] = not can_caseworker_edit_role
        self.fields["team"].widget.attrs["disabled"] = not can_caseworker_edit_team
        self.fields["role"].required = can_caseworker_edit_role
        self.fields["team"].required = can_caseworker_edit_team

        self.fields["team"].choices = [Choice(t["id"], t["name"]) for t in teams]
        self.fields["role"].choices = [Choice(r["id"], r["name"]) for r in roles]
        queues_choice = []
        for q in queues:
            team_id = None
            if q.get("team"):
                team_id = q.get("team").get("id")
            queues_choice.append(Choice(value=q["id"], label=q["name"], attr={"data-attribute": team_id}))

        self.fields["default_queue"].choices = queues_choice

    def clean(self):
        cleaned_data = super().clean()
        for field in ["role", "team"]:
            if self.fields["role"].widget.attrs["disabled"] == True:
                del cleaned_data[field]
        return cleaned_data

    def _clean_for_readonly_field(self, fname):
        """will reset value to initial - nothing will be changed
        needs to be added dynamically - partial, see init_fields
        """
        return self.initial[fname]  # or getattr(self.instance, fname)

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
            "default_queue",
        )
