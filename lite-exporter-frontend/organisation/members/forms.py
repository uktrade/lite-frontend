from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink, Checkboxes
from lite_forms.helpers import conditional
from organisation.roles.services import get_roles
from organisation.sites.services import get_sites


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
            Checkboxes(
                title=strings.users.AddUserForm.ASSIGN_USER_QUESTION,
                name="sites[]",
                options=get_sites(request, request.user.organisation, True),
            ),
        ],
        back_link=BackLink(
            strings.users.AddUserForm.USER_ADD_FORM_BACK_TO_USERS, reverse_lazy("organisation:members:members")
        ),
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
            strings.users.EditUserForm.USER_EDIT_FORM_BACK_TO_USER,
            reverse_lazy("organisation:members:user", kwargs={"pk": user_id}),
        ),
        default_button_name=strings.users.EditUserForm.USER_EDIT_FORM_SAVE,
    )


def assign_sites(request):
    return Form(
        title=strings.users.AssignToSitesForm.ASSIGN_USER_TO_SITES_TITLE,
        description=strings.users.AssignToSitesForm.ASSIGN_USER_TO_SITES_DESCRIPTION,
        questions=[Checkboxes(name="sites[]", options=get_sites(request, request.user.organisation, True))],
        default_button_name=strings.SAVE,
    )
