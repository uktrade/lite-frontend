from django.urls import reverse_lazy
from lite_forms.helpers import conditional

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink
from roles.services import get_roles


def add_user_form(request):
    return Form(
        title=strings.users.AddUserForm.USER_ADD_TITLE,
        questions=[
            TextInput(title=strings.users.AddUserForm.USER_EMAIL_QUESTION, name="email"),
            Select(
                name="role",
                options=get_roles(request, request.user.organisation, True),
                title=strings.users.AddUserForm.USER_ROLE_QUESTION,
                include_default_select=False,
            ),
        ],
        back_link=BackLink(strings.users.AddUserForm.USER_ADD_FORM_BACK_TO_USERS, reverse_lazy("users:users")),
    )


def edit_user_form(request, user_id, can_edit_role: bool):
    return Form(
        title=strings.users.EditUserForm.USER_EDIT_TITLE,
        questions=[
            conditional(
                can_edit_role,
                Select(
                    name="role",
                    options=get_roles(request, request.user.organisation, True),
                    title=strings.users.EditUserForm.USER_ROLE_QUESTION,
                    include_default_select=False,
                ),
            ),
        ],
        back_link=BackLink(
            strings.users.EditUserForm.USER_EDIT_FORM_BACK_TO_USER, reverse_lazy("users:user", kwargs={"pk": user_id})
        ),
        default_button_name=strings.users.EditUserForm.USER_EDIT_FORM_SAVE,
    )
