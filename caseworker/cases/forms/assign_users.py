from django.http import HttpRequest
from django.urls import reverse, reverse_lazy

from caseworker.core.constants import UserStatuses
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import (
    Checkboxes,
    Filter,
    Form,
    RadioButtons,
    Button,
    HiddenField,
    BackLink,
    DetailComponent,
    TextArea,
)
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle
from caseworker.teams.services import get_users_team_queues
from caseworker.users.services import get_gov_users


def assign_users_form(request: HttpRequest, team_id, queue, multiple: bool):
    params = {"teams": team_id, "disable_pagination": True, "status": UserStatuses.ACTIVE}
    return Form(
        title=cases.Manage.AssignUsers.MULTIPLE_TITLE if multiple else cases.Manage.AssignUsers.TITLE,
        description=cases.Manage.AssignUsers.DESCRIPTION,
        questions=[
            Filter(),
            Checkboxes(
                "users",
                options=get_gov_users(
                    request,
                    params,
                    convert_to_options=True,
                ),
                filterable=True,
            ),
            DetailComponent(
                title=cases.Manage.AssignUsers.NOTE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        caption=queue["name"],
        default_button_name=cases.Manage.AssignUsers.BUTTON,
    )


def assign_case_officer_form(request: HttpRequest, existing_officer, queue_id, case_id, is_compliance=None):
    params = {"disable_pagination": True, "status": UserStatuses.ACTIVE}
    users = get_gov_users(request, params, convert_to_options=True)
    buttons = [Button(cases.Manage.AssignCaseOfficer.SUBMIT_BUTTON, action="submit")]
    if existing_officer:
        buttons.append(
            Button(
                conditional(
                    is_compliance,
                    cases.Manage.AssignCaseOfficer.DELETE_INSPECTOR_BUTTON,
                    cases.Manage.AssignCaseOfficer.DELETE_BUTTON,
                ),
                action="delete",
                id="unassign",
                style=ButtonStyle.WARNING,
            )
        )

    return Form(
        title=conditional(
            is_compliance, cases.Manage.AssignCaseOfficer.INSPECTOR_TITLE, cases.Manage.AssignCaseOfficer.TITLE
        ),
        description=cases.Manage.AssignCaseOfficer.DESCRIPTION,
        questions=[Filter(), RadioButtons("gov_user_pk", users, filterable=True)],
        buttons=buttons,
        container="case",
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id, "tab": "details"})),
    )


def assign_user_and_work_queue(request, queue_id, case_id):
    user_params = {"disable_pagination": True, "status": UserStatuses.ACTIVE}
    users = get_gov_users(request, user_params, convert_to_options=True)
    return Form(
        title=cases.Manage.AssignUserAndQueue.USER_TITLE,
        description=cases.Manage.AssignUserAndQueue.USER_DESCRIPTION,
        questions=[Filter(), RadioButtons("user", users, filterable=True)],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id})),
        default_button_name=strings.CONTINUE,
        container="case",
    )


def users_team_queues(request, queue_pk, case_pk, user_pk):
    queues = get_users_team_queues(request, user_pk, True)
    return Form(
        title=cases.Manage.AssignUserAndQueue.QUEUE_TITLE,
        description=cases.Manage.AssignUserAndQueue.QUEUE_DESCRIPTION,
        questions=[
            Filter(),
            RadioButtons("queue", queues, filterable=True),
            HiddenField("user_pk", user_pk),
            HiddenField("case_pk", case_pk),
            DetailComponent(
                title=cases.Manage.AssignUserAndQueue.NOTE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        back_link=BackLink(url=reverse_lazy("cases:assign_user", kwargs={"queue_pk": queue_pk, "pk": case_pk})),
        container="case",
    )
