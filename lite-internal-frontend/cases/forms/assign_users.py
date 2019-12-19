from lite_content.lite_internal_frontend import strings
from django.http import HttpRequest
from lite_forms.components import Checkboxes, Filter, Form

from users.services import get_gov_users


def assign_users_form(request: HttpRequest, team_id, queue, multiple: bool):
    return Form(
        title=strings.Cases.Manage.AssignUsers.MULTIPLE_TITLE if multiple else strings.Cases.Manage.AssignUsers.TITLE,
        description=strings.Cases.Manage.AssignUsers.DESCRIPTION,
        questions=[Filter(), Checkboxes("users", get_gov_users(request, {"teams": team_id}, convert_to_options=True))],
        caption=queue["name"],
        default_button_name="Submit",
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
    )
