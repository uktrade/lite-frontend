from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink
from lite_forms.helpers import conditional
from teams.services import get_teams
from users.services import get_roles


def add_user_form(request):
    return Form(
        title=strings.USER_ADD_TITLE,
        questions=[
            TextInput(title=strings.USER_EMAIL_QUESTION, name="email"),
            Select(name="team", title=strings.USER_TEAM_QUESTION, options=get_teams(request, True)),
            Select(name="role", options=get_roles(request, True), title=strings.USER_ROLE_QUESTION),
        ],
        back_link=BackLink(strings.USER_ADD_FORM_BACK_TO_USERS, reverse_lazy("users:users")),
    )


def edit_user_form(request, user_id, can_edit_role: bool):
    return Form(
        title="Edit User",
        questions=[
            TextInput(title=strings.USER_EMAIL_QUESTION, name="email"),
            Select(name="team", title=strings.USER_TEAM_QUESTION, options=get_teams(request, True)),
            conditional(
                can_edit_role, Select(name="role", options=get_roles(request, True), title=strings.USER_ROLE_QUESTION),
            ),
        ],
        back_link=BackLink(strings.USER_EDIT_FORM_BACK_TO_USER, reverse_lazy("users:user", kwargs={"pk": user_id})),
        default_button_name=strings.USER_EDIT_FORM_SAVE,
    )
