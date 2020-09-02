from django.urls import reverse_lazy

from exporter.core.constants import SUPER_USER_ROLE_ID, DEFAULT_USER_ROLE_ID
from lite_forms.views import SingleFormView
from exporter.organisation.members.services import get_user
from exporter.organisation.roles.forms import add_role
from exporter.organisation.roles.services import get_roles, get_permissions, post_role, put_role, get_role
from exporter.organisation.views import OrganisationView


class Roles(OrganisationView):
    template_name = "roles/index"

    def get_additional_context(self):
        user = get_user(self.request)
        user_role_id = user["role"]["id"]
        roles = get_roles(self.request, self.organisation_id, page=self.request.GET.get("page", 1))
        all_permissions = get_permissions(self.request)

        return {
            "roles": roles,
            "user_role_id": user_role_id,
            "immutable_roles": [SUPER_USER_ROLE_ID, DEFAULT_USER_ROLE_ID],
            "all_permissions": all_permissions,
        }


class AddRole(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_role(request, add=True)
        self.action = post_role
        self.success_url = reverse_lazy("organisation:roles:roles")


class EditRole(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_role(request, self.object_pk)
        self.form = add_role(request, add=False)
        self.action = put_role
        self.success_url = reverse_lazy("organisation:roles:roles")
