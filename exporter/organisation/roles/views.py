from core.constants import ExporterRoles as Rolestuple
from exporter.organisation.members.services import get_user
from exporter.organisation.roles.services import get_roles, get_permissions
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
            "immutable_roles": [role.id for role in Rolestuple.immutable_roles],
            "all_permissions": all_permissions,
        }
