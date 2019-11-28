from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import Permissions, SUPER_USER_ROLE_ID
from core.services import get_organisation_users, get_organisation, get_organisation_user, put_organisation_user
from lite_forms.views import SingleFormView
from roles.services import get_user_permissions
from users.forms import add_user_form, edit_user_form
from users.services import post_users, get_user, is_super_user


class Users(TemplateView):
    def get(self, request, **kwargs):
        users, _ = get_organisation_users(request, str(request.user.organisation))
        organisation = get_organisation(request, str(request.user.organisation))
        user_permissions = get_user_permissions(request)

        sites, roles = False, False
        if Permissions.ADMINISTER_SITES in user_permissions:
            sites = True

        if Permissions.EXPORTER_ADMINISTER_ROLES in user_permissions:
            roles = True

        if organisation["type"]["key"] == "individual":
            raise Http404

        context = {
            "title": "Users - " + organisation["name"],
            "users": users["users"],
            "organisation": organisation,
            "can_administer_roles": roles,
            "can_administer_sites": sites,
        }
        return render(request, "users/index.html", context)


class AddUser(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_user_form(request)
        self.success_url = reverse_lazy("users:users")
        self.action = post_users


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        user = get_organisation_user(request, str(request.user.organisation), str(kwargs["pk"]))
        request_user, _ = get_user(request)
        super_user = is_super_user(request_user)
        can_deactivate = not is_super_user(user)

        context = {
            "profile": user["user"],
            "super_user": super_user,
            "super_user_role_id": SUPER_USER_ROLE_ID,
            "can_deactivate": can_deactivate,
        }
        return render(request, "users/profile.html", context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        user = request.user
        return redirect(reverse_lazy("users:user", kwargs={"pk": user.lite_api_user_id}))


class EditUser(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        user = get_organisation_user(request, str(request.user.organisation), str(self.object_pk))
        super_user = is_super_user(user) and request.user.lite_api_user_id == str(kwargs["pk"])
        self.form = edit_user_form(request, self.object_pk, super_user)
        self.data = user["user"]
        self.action = put_organisation_user
        self.success_url = reverse_lazy("users:user", kwargs={"pk": self.object_pk})


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = (
                "This user will no longer be able to log in or perform tasks on LITE " "on behalf of your organisation."
            )

        if status == "reactivate":
            description = (
                "This user will be able to log in to and perform tasks on LITE on behalf " "of your organisation."
            )

        context = {
            "title": "Are you sure you want to {} this user?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "users/change_status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_organisation_user(request, str(kwargs["pk"]), request.POST)

        return redirect("/users/")
