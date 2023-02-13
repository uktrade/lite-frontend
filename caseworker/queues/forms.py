from storages.backends.s3boto3 import S3Boto3StorageFile

from django import forms
from django.urls import reverse_lazy
from django.db import models

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML
from django.template.loader import render_to_string

from core.common.forms import TextChoice, BaseForm

from lite_content.lite_internal_frontend.queues import AddQueueForm, EditQueueForm
from lite_forms.components import Form, TextInput, BackLink, Select
from caseworker.queues.services import get_queues
from caseworker.users.services import get_gov_users
from caseworker.core.constants import UserStatuses


def new_queue_form(request):
    return Form(
        title=AddQueueForm.TITLE,
        description=AddQueueForm.DESCRIPTION,
        questions=[
            TextInput(
                title=AddQueueForm.Name.TITLE,
                description=AddQueueForm.Name.DESCRIPTION,
                name="name",
            ),
            Select(
                title=AddQueueForm.CountersigningQueue.TITLE,
                description=AddQueueForm.CountersigningQueue.DESCRIPTION,
                options=get_queues(
                    request=request, disable_pagination=True, convert_to_options=True, users_team_first=True
                ),
                name="countersigning_queue",
            ),
        ],
        back_link=BackLink(AddQueueForm.BACK, reverse_lazy("queues:manage")),
    )


def remove_current_queue_id(options, queue_id):
    new_options = options
    for option in new_options:
        if option.key == str(queue_id):
            new_options.remove(option)
            break

    return new_options


def edit_queue_form(request, queue_id):
    return Form(
        title=EditQueueForm.TITLE,
        description=EditQueueForm.DESCRIPTION,
        questions=[
            TextInput(
                title=EditQueueForm.Name.TITLE,
                description=EditQueueForm.Name.DESCRIPTION,
                name="name",
            ),
            Select(
                title=EditQueueForm.CountersigningQueue.TITLE,
                description=EditQueueForm.CountersigningQueue.DESCRIPTION,
                options=remove_current_queue_id(
                    get_queues(
                        request=request, disable_pagination=True, convert_to_options=True, users_team_first=True
                    ),
                    queue_id,
                ),
                name="countersigning_queue",
            ),
        ],
        back_link=BackLink(EditQueueForm.BACK, reverse_lazy("queues:manage")),
    )


class EnforcementXMLImportForm(forms.Form):

    file = forms.FileField(label="Upload a file", widget=forms.FileInput(attrs={"accept": "text/xml"}))

    # the CreateView expects `instance` to be passed in here
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_file(self):
        value = self.cleaned_data["file"]
        if isinstance(value, S3Boto3StorageFile):
            s3_obj = value.obj.get()["Body"]
            return s3_obj.read().decode("utf-8")

        return value.read().decode("utf-8")

    def save(self):
        # the CreateView expects this method
        pass


class CaseAssignmentsCaseOfficerForm(BaseForm):
    class Layout:
        TITLE = "Who do you want to allocate as Licensing Unit case officer ?"
        SUBTITLE = "Manages the case until the application outcome (the exporter will see this name until the case officer is changed)"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    users = forms.ChoiceField(
        label="",
        choices=(),  # set in __init__
        required=True,
        error_messages={
            "required": "Select a user to allocate as Licensing Unit case officer",
        },
        widget=forms.RadioSelect,
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
            HTML(render_to_string("forms/filter_radios.html")),
            "users",
        )


class SelectAllocateRole(BaseForm):
    class Layout:
        TITLE = "Which role do you want to allocate ?"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    class RoleChoices(models.TextChoices):
        CASE_ADVISOR = "CASE_ADVISOR", "Case advisor"
        LU_CASE_OFFICER = "LU_CASE_OFFICER", "Licensing unit case officer"

    ROLE_CHOICES = (
        TextChoice(RoleChoices.CASE_ADVISOR, hint="Reviews or gives advice on the case while it is with your team"),
        TextChoice(
            RoleChoices.LU_CASE_OFFICER,
            hint="Manages the case until the application outcome (the exporter will see this name until the case officer is changed)",
        ),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select case adviser or Licensing Unit case officer"},
    )

    def get_layout_fields(self):
        return ("role",)
