from django.http import HttpRequest
from lite_forms.components import Checkboxes, Filter, Form

from core.builtins.custom_tags import get_string
from users.services import get_gov_users


def assign_users_form(request: HttpRequest, team_id, queue, multiple: bool):
    return Form(
        title=get_string("cases.manage.assign_users.multiple_title")
        if multiple
        else get_string("cases.manage.assign_users.title"),
        description=get_string("cases.manage.assign_users.description"),
        questions=[Filter(), Checkboxes("users", get_gov_users(request, {"teams": team_id}, convert_to_options=True))],
        caption=queue["name"],
        default_button_name="Submit",
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
    )
