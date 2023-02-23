import logging
from http import HTTPStatus

from django.urls import reverse
from django.shortcuts import redirect

from core.decorators import expect_status

from core.wizard.views import BaseSessionWizardView
from exporter.organisation.sites.services import get_sites

from exporter.organisation.members.services import post_users
from exporter.core.services import get_organisation_users_list

from core.auth.views import LoginRequiredMixin
from .constants import AddUserSteps
from .payloads import AddMemberPayloadBuilder
from .conditional import is_agent_role

from .forms import (
    SelectRoleForm,
    AddUserForm,
    AgentDeclarationForm,
)

logger = logging.getLogger(__name__)


class AddUser(
    BaseSessionWizardView,
    LoginRequiredMixin,
):
    form_list = [
        (AddUserSteps.SELECT_ROLE, SelectRoleForm),
        (AddUserSteps.ADD_MEMBER, AddUserForm),
        (AddUserSteps.AGENT_DECLARATION, AgentDeclarationForm),
    ]
    condition_dict = {AddUserSteps.AGENT_DECLARATION: is_agent_role}

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddUserSteps.ADD_MEMBER:
            users = get_organisation_users_list(self.request, str(self.request.session["organisation"]))
            organisation_users = set(user["email"] for user in users)
            kwargs["organisation_users"] = organisation_users
            kwargs["sites"] = get_sites(self.request, self.request.session["organisation"])
            kwargs["role_id"] = self.role_id
        return kwargs

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding user to organisation",
        "Unexpected error adding user to organisation",
    )
    def post_add_user(self, form_dict):
        payload = AddMemberPayloadBuilder().build(form_dict)
        return post_users(self.request, payload)

    def done(self, form_list, form_dict, **kwargs):
        self.post_add_user(form_dict)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("organisation:members:members")

    @property
    def role_id(self):
        return self.get_cleaned_data_for_step(AddUserSteps.SELECT_ROLE)["role"]
