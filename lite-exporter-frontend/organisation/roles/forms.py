from django.http import HttpRequest
from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, TextInput, Checkboxes, BackLink
from organisation.roles.services import get_permissions


def add_role(request: HttpRequest, add: bool):
    if add:
        form_strings = strings.roles.AddRoleForm
    else:
        form_strings = strings.roles.EditRoleForm

    return Form(
        title=form_strings.TITLE,
        description=form_strings.DESCRIPTION,
        questions=[
            TextInput(title=form_strings.NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=form_strings.PERMISSIONS,
                description=form_strings.PERMISSIONS_DESCRIPTION,
            ),
        ],
        back_link=BackLink(form_strings.FORM_BACK_TO_ROLES, reverse_lazy("organisation:roles:roles")),
        default_button_name=form_strings.FORM_CREATE,
    )
