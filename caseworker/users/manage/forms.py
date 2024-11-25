from django import forms

from core.common.forms import BaseForm
from core.forms.widgets import FilterSelect
from crispy_forms_gds.choices import Choice
from caseworker.users.services import get_gov_user_list


class BaseCaseworkerUser(BaseForm):

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

    def get_layout_fields(self):
        return (
            "email",
            "role",
            "team",
            "default_queue",
        )

    def __init__(self, request, teams, roles, queues, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["team"].choices = [Choice(t["id"], t["name"]) for t in teams]
        self.fields["role"].choices = [Choice(r["id"], r["name"]) for r in roles]

        get_team_id = lambda q: q.get("team").get("id") if q.get("team") else None

        self.fields["default_queue"].choices = [
            Choice(value=q["id"], label=q["name"], attrs={"data-attribute": get_team_id(q)}) for q in queues
        ]
        self.fields["default_queue"].choices.insert(0, Choice(None, "Select"))

    def validate_email_duplicates(self, email):
        gov_user_list = get_gov_user_list(self.request, {"email": email})
        if gov_user_list["count"]:
            raise forms.ValidationError("This email has already been registered")


class EditCaseworkerQueue(BaseCaseworkerUser):
    class Layout:
        TITLE = "Edit"
        SUBMIT_BUTTON_TEXT = "Save and return"

    _editable_fields = ["email", "team", "role"]

    def __init__(self, request, teams, roles, queues, *args, **kwargs):
        super().__init__(request, teams, roles, queues, *args, **kwargs)

        self._email_changed = False
        for field in self._editable_fields:
            self.fields[field].disabled = True
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        for field in self._editable_fields:
            del cleaned_data[field]
        return cleaned_data


class EditCaseworker(BaseCaseworkerUser):
    class Layout:
        TITLE = "Edit"
        SUBMIT_BUTTON_TEXT = "Save and return"

    def __init__(self, request, teams, roles, queues, *args, **kwargs):
        super().__init__(request, teams, roles, queues, *args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"] or self.initial["email"]
        if email != self.initial["email"].lower():
            self.validate_email_duplicates(email)
        return email


class AddCaseworkerUser(BaseCaseworkerUser):
    class Layout:
        TITLE = "Invite a user"
        SUBMIT_BUTTON_TEXT = "Save"

    def __init__(self, request, teams, roles, queues, *args, **kwargs):
        super().__init__(request, teams, roles, queues, *args, **kwargs)
        self.fields["team"].choices.insert(0, Choice(None, "Select"))
        self.fields["role"].choices.insert(0, Choice(None, "Select"))

    def clean_email(self):
        email = self.cleaned_data["email"] or self.initial["email"]
        self.validate_email_duplicates(email)
        return email
