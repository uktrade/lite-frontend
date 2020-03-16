from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.users import AddUserForm, EditUserForm
from lite_forms.components import Form, Select, TextInput, BackLink
from lite_forms.helpers import conditional
from teams.services import get_teams
from users.services import get_roles


def add_user_form(request):
    return Form(
        title=AddUserForm.TITLE,
        questions=[
            TextInput(title=AddUserForm.Email.TITLE, description=AddUserForm.Email.DESCRIPTION, name="email"),
            Select(
                title=AddUserForm.Team.TITLE,
                description=AddUserForm.Team.DESCRIPTION,
                name="team",
                options=get_teams(request, True),
            ),
            Select(
                title=AddUserForm.Role.TITLE,
                description=AddUserForm.Role.DESCRIPTION,
                name="role",
                options=get_roles(request, True),
            ),
        ],
        back_link=BackLink(AddUserForm.BACK_LINK, reverse_lazy("users:users")),
    )


def edit_user_form(request, user, can_edit_role: bool):
    return Form(
        title=EditUserForm.TITLE.format(user["first_name"], user["last_name"]),
        questions=[
            TextInput(title=EditUserForm.Email.TITLE, description=EditUserForm.Email.DESCRIPTION, name="email"),
            Select(
                title=EditUserForm.Team.TITLE,
                description=EditUserForm.Team.DESCRIPTION,
                name="team",
                options=get_teams(request, True),
            ),
            conditional(
                can_edit_role,
                Select(
                    title=EditUserForm.Role.TITLE,
                    description=EditUserForm.Role.DESCRIPTION,
                    name="role",
                    options=get_roles(request, True),
                ),
            ),
        ],
        back_link=BackLink(
            EditUserForm.BACK_LINK.format(user["first_name"], user["last_name"]),
            reverse_lazy("users:user", kwargs={"pk": user["id"]}),
        ),
        default_button_name=EditUserForm.SUBMIT_BUTTON,
    )
