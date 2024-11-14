from django import forms

from core.common.forms import BaseForm
from core.forms.widgets import FilterSelect
from crispy_forms_gds.choices import Choice
from caseworker.users.services import get_gov_user_list


class EditCaseworkerUser(BaseForm):
    class Layout:
        TITLE = "Edit"
        SUBMIT_BUTTON_TEXT = "Save and return"

    _editable_fields = ["email", "team", "role"]

    email = forms.EmailField(
        label="Email",
        error_messages={
            "required": "Enter an email address in the correct format, like name@example.com",
        },
    )

    role = forms.ChoiceField(
        label="Role",
        widget=forms.Select(attrs={"id": "role"}),
    )

    team = forms.ChoiceField(label="Team", widget=forms.Select(attrs={"id": "team"}))

    default_queue = forms.ChoiceField(
        label="Default Queue",
        widget=FilterSelect(
            parent_select_name="team",
            attrs={"id": "default_queue", "class": "govuk-select"},
        ),
    )

    def __init__(self, request, teams, roles, queues, can_caseworker_edit_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = not can_caseworker_edit_user
        self.request = request
        self._email_changed = False
        if self.read_only:
            for field in self._editable_fields:
                self.fields[field].widget.attrs["disabled"] = True
                self.fields[field].required = False

        self.fields["team"].choices = [Choice(t["id"], t["name"]) for t in teams]
        self.fields["role"].choices = [Choice(r["id"], r["name"]) for r in roles]

        get_team_id = lambda q: q.get("team").get("id") if q.get("team") else None

        self.fields["default_queue"].choices = [
            Choice(value=q["id"], label=q["name"], attrs={"data-attribute": get_team_id(q)}) for q in queues
        ]
        self.fields["default_queue"].choices.insert(0, Choice(None, "Select"))

    def clean(self):
        cleaned_data = super().clean()
        if self.read_only:
            for field in self._editable_fields:
                del cleaned_data[field]
        return cleaned_data

    def clean_email(self):

        email = self.cleaned_data["email"] or self.initial["email"]
        if not self.read_only:
            email_changed = email != self.initial["email"].lower()
            if email_changed:
                gov_user_list = get_gov_user_list(self.request, {"email": email})
                if gov_user_list["count"]:
                    raise forms.ValidationError("This email has already been registered")
        return email

    def get_layout_fields(self):
        return (
            "email",
            "role",
            "team",
            "default_queue",
        )
