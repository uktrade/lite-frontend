from django import forms

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML
from django.template.loader import render_to_string

from core.common.forms import TextChoice, BaseForm

from caseworker.core.constants import UserStatuses
from caseworker.users.services import get_gov_users
from caseworker.teams.services import get_users_team_queues


class CaseAssignmentRemove(forms.Form):
    assignment_id = forms.CharField(widget=forms.HiddenInput)


class CaseAssignmentUsersForm(BaseForm):
    class Layout:
        TITLE = "Which users do you want to assign to this case?"
        SUBMIT_BUTTON_TEXT = "Save"

    users = forms.MultipleChoiceField(
        label="",
        choices=(),  # set in __init__
        required=True,
        error_messages={
            "required": "Select a user to allocate",
        },
        widget=forms.CheckboxSelectMultiple,
    )
    note = forms.CharField(
        label="Explain why you're allocating these users (optional)",
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False,
    )

    def __init__(self, request, team_id, *args, **kwargs):
        self.request = request
        self.team_id = team_id
        self.declared_fields["users"].choices = self.get_user_choices()
        super().__init__(*args, **kwargs)

    def get_user_choices(self):
        user_params = {"teams": self.team_id, "disable_pagination": True, "status": UserStatuses.ACTIVE}

        team_users, _ = get_gov_users(self.request, user_params)
        return [
            (
                TextChoice(
                    Choice(
                        user["id"],
                        user.get("first_name") + " " + user.get("last_name")
                        if user.get("first_name")
                        else user["email"],
                    ),
                    hint=user["email"],
                )
            )
            for user in team_users["results"]
        ]

    def get_layout_fields(self):

        return (
            HTML(render_to_string("forms/filter_checkboxes.html")),
            "users",
            "note",
        )


class CaseAssignmentQueueForm(BaseForm):
    class Layout:
        TITLE = "Select a team queue to add the case to"
        SUBMIT_BUTTON_TEXT = "Save"

    queue = forms.ChoiceField(
        label="",
        choices=(),  # set in __init__
        required=True,
        error_messages={
            "required": "Select a queue to add the case to",
        },
        widget=forms.RadioSelect,
    )

    def __init__(self, request, user_id, *args, **kwargs):
        self.request = request
        self.user_id = user_id
        self.declared_fields["queue"].choices = self.get_queue_choices()
        super().__init__(*args, **kwargs)

    def get_queue_choices(self):
        queues, _ = get_users_team_queues(self.request, self.user_id, False)
        return [
            (
                TextChoice(
                    Choice(queue_id, queue_name),
                )
            )
            for queue_id, queue_name in queues["queues"]
        ]

    def get_layout_fields(self):

        return (
            HTML(render_to_string("forms/filter_radios.html")),
            "queue",
        )
