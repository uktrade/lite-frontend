from core.services import get_statuses
from lite_content.lite_internal_frontend.roles import AddRoleForm, EditRoleForm
from django.http import HttpRequest
from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, Checkboxes, BackLink

from users.services import get_permissions


def add_role(request: HttpRequest):
    return Form(
        title=AddRoleForm.TITLE,
        description=AddRoleForm.DESCRIPTION,
        questions=[
            TextInput(title=AddRoleForm.ROLE_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=AddRoleForm.PERMISSION_CHECKBOXES_TITLE,
                description=AddRoleForm.PERMISSION_CHECKBOXES_DESCRIPTION,
                optional=True,
                classes=["govuk-checkboxes--small"],
            ),
            Checkboxes(
                name="statuses[]",
                options=get_statuses(request, True),
                title=AddRoleForm.STATUSES_CHECKBOXES_TITLE,
                description=AddRoleForm.STATUSES_CHECKBOXES_DESCRIPTION,
                optional=True,
                classes=["govuk-checkboxes--small"],
            ),
        ],
        back_link=BackLink(AddRoleForm.BACK_LINK, reverse_lazy("users:roles")),
        default_button_name=AddRoleForm.FORM_CREATE,
    )


def edit_role(request: HttpRequest):
    return Form(
        title=EditRoleForm.TITLE,
        description=EditRoleForm.DESCRIPTION,
        questions=[
            TextInput(title=EditRoleForm.ROLE_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=EditRoleForm.PERMISSION_CHECKBOXES_TITLE,
                description=EditRoleForm.PERMISSION_CHECKBOXES_DESCRIPTION,
                optional=True,
                classes=["govuk-checkboxes--small"],
            ),
            Checkboxes(
                name="statuses[]",
                options=get_statuses(request, True),
                title=AddRoleForm.STATUSES_CHECKBOXES_TITLE,
                description=AddRoleForm.STATUSES_CHECKBOXES_DESCRIPTION,
                optional=True,
                classes=["govuk-checkboxes--small"],
            ),
        ],
        back_link=BackLink(EditRoleForm.BACK_LINK, reverse_lazy("users:roles")),
        default_button_name=EditRoleForm.FORM_CREATE,
    )
