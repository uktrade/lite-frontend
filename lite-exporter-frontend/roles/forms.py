from django.http import HttpRequest
from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, TextInput, Checkboxes, BackLink
from roles.services import get_permissions


def add_role(request: HttpRequest):
    return Form(
        title=strings.ADD_ROLE_TITLE,
        description=strings.ADD_ROLE_DESCRIPTION,
        questions=[
            TextInput(title=strings.ROLES_ADD_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=strings.ROLES_ADD_PERMISSIONS,
                description=strings.ROLES_ADD_PERMISSIONS_DESCRIPTION,
            ),
        ],
        back_link=BackLink(strings.ROLES_ADD_FORM_BACK_TO_ROLES, reverse_lazy("roles:roles")),
        default_button_name=strings.ROLES_ADD_FORM_CREATE,
    )


def edit_role(request: HttpRequest):
    return Form(
        title=strings.EDIT_ROLE_TITLE,
        description=strings.EDIT_ROLE_DESCRIPTION,
        questions=[
            TextInput(title=strings.ROLES_EDIT_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=strings.ROLES_EDIT_PERMISSIONS,
                description=strings.ROLES_EDIT_PERMISSIONS_DESCRIPTION,
            ),
        ],
        back_link=BackLink(strings.ROLES_EDIT_FORM_BACK_TO_ROLES, reverse_lazy("roles:roles")),
        default_button_name=strings.ROLES_EDIT_FORM_CREATE,
    )
