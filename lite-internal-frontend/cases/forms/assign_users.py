from conf.constants import UserStatuses
from lite_content.lite_internal_frontend import strings
from lite_forms.styles import ButtonStyle

from lite_content.lite_internal_frontend.strings import cases
from django.http import HttpRequest
from lite_forms.components import Checkboxes, Filter, Form, RadioButtons, Button, HiddenField
from teams.services import get_users_teams

from users.services import get_gov_users


def assign_users_form(request: HttpRequest, team_id, queue, multiple: bool):
    params = {"teams": team_id, "disable_pagination": True, "status": UserStatuses.ACTIVE}
    return Form(
        title=cases.Manage.AssignUsers.MULTIPLE_TITLE if multiple else cases.Manage.AssignUsers.TITLE,
        description=cases.Manage.AssignUsers.DESCRIPTION,
        questions=[Filter(), Checkboxes("users", get_gov_users(request, params, convert_to_options=True))],
        caption=queue["name"],
        default_button_name=cases.Manage.AssignUsers.BUTTON,
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
    )


def assign_case_officer_form(request: HttpRequest, existing_officer):
    params = {"disable_pagination": True, "status": UserStatuses.ACTIVE}
    users = get_gov_users(request, params, convert_to_options=True)
    buttons = [Button(cases.Manage.AssignCaseOfficer.SUBMIT_BUTTON, action="submit")]
    if existing_officer:
        buttons.append(
            Button(
                cases.Manage.AssignCaseOfficer.DELETE_BUTTON, action="delete", id="unassign", style=ButtonStyle.WARNING
            )
        )

    return Form(
        title=cases.Manage.AssignCaseOfficer.TITLE,
        description=cases.Manage.AssignCaseOfficer.DESCRIPTION,
        questions=[Filter(), RadioButtons("user", users)],
        buttons=buttons,
        javascript_imports=["/assets/javascripts/filter-radiobuttons-list.js"],
    )


def assign_user_and_work_queue(request):
    user_params = {"disable_pagination": True, "status": UserStatuses.ACTIVE}
    users = get_gov_users(request, user_params, convert_to_options=True)
    return Form(
        title=cases.Manage.AssignUserAndQueue.USER_TITLE,
        description=cases.Manage.AssignUserAndQueue.USER_DESCRIPTION,
        questions=[Filter(), RadioButtons("user", users)],
        default_button_name=strings.CONTINUE,
        javascript_imports=["/assets/javascripts/filter-radiobuttons-list.js"],
    )


def users_team_queues(request, case_pk, user_pk):
    queues = get_users_teams(request, user_pk, True)
    return Form(
        title=cases.Manage.AssignUserAndQueue.QUEUE_TITLE,
        description=cases.Manage.AssignUserAndQueue.QUEUE_DESCRIPTION,
        questions=[
            Filter(),
            RadioButtons("queue", queues),
            HiddenField("user_pk", user_pk),
            HiddenField("case_pk", case_pk),
        ],
        javascript_imports=["/assets/javascripts/filter-radiobuttons-list.js"],
    )
