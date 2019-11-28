from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import SUPER_USER_ROLE_ID, DEFAULT_USER_ROLE_ID, Permissions
from lite_forms.views import SingleFormView
from roles.forms import add_role, edit_role
from roles.services import get_roles, put_role, get_role, post_role, get_permissions, get_user_permissions


class Roles(TemplateView):
    def get(self, request, **kwargs):
        organisation_id = str(request.user.organisation)
        roles = get_roles(request, organisation_id)
        all_permissions = get_permissions(request)
        user_permissions = get_user_permissions(request)

        users, sites = False, False
        if Permissions.ADMINISTER_USERS in user_permissions:
            users = True

        if Permissions.ADMINISTER_SITES in user_permissions:
            sites = True

        context = {
            "all_permissions": all_permissions,
            "roles": roles,
            "user_permissions": user_permissions,
            "immutable_roles": [SUPER_USER_ROLE_ID, DEFAULT_USER_ROLE_ID],
            "can_administer_sites": sites,
            "can_administer_users": users,
        }
        return render(request, "roles/index.html", context)


class AddRole(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_role(request)
        self.action = post_role
        self.success_url = reverse_lazy("roles:roles")


class EditRole(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_role(request, self.object_pk)
        self.form = edit_role(request)
        self.action = put_role
        self.success_url = reverse_lazy("roles:roles")
