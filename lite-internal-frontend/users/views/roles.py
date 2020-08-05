from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from conf.constants import SUPER_USER_ROLE_ID
from core.services import get_user_permissions
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.roles import ManageRolesPage
from lite_forms.views import SingleFormView
from users.forms.roles import add_role, edit_role
from users.services import get_roles, get_permissions, get_role, put_role, post_role, get_gov_user


class Roles(TemplateView):
    def get(self, request, **kwargs):
        roles, _ = get_roles(request)
        all_permissions = get_permissions(request)
        permissions = get_user_permissions(request)
        user, _ = get_gov_user(request)

        context = {
            "all_permissions": all_permissions,
            "roles": roles["roles"],
            "title": strings.roles.ManageRolesPage.TITLE,
            "user_permissions": permissions,
            "super_user_role_id": SUPER_USER_ROLE_ID,
            "user_role_id": user["user"]["role"]["id"],
        }
        return render(request, "users/roles.html", context)


class AddRole(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_role(request)
        self.action = post_role

    def get_success_url(self):
        messages.success(self.request, ManageRolesPage.SUCCESS_MESSAGE)
        return reverse("users:roles")


class EditRole(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        role, _ = get_role(request, self.object_pk)
        self.form = edit_role(request)
        self.data = role["role"]
        self.action = put_role
        self.success_url = reverse("users:roles")
