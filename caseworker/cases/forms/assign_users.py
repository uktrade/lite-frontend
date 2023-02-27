from django.http import HttpRequest
from django.urls import reverse

from caseworker.core.constants import UserStatuses
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import (
    Filter,
    Form,
    RadioButtons,
    Button,
    BackLink,
)
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle
from caseworker.users.services import get_gov_users


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
