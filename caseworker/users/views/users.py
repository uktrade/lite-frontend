from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from caseworker.core.constants import SUPER_USER_ROLE_ID, UserStatuses
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.users import UsersPage
from lite_forms.components import FiltersBar, Select, Option, TextInput
from lite_forms.views import SingleFormView
from caseworker.users.forms.users import add_user_form, edit_user_form
from caseworker.users.services import (
    get_gov_users,
    post_gov_users,
    put_gov_user,
    get_gov_user,
    is_super_user,
)


class UsersList(TemplateView):
    def get(self, request, **kwargs):
        params = {
            "page": int(self.request.GET.get("page", 1)),
            "email": self.request.GET.get("email", ""),
            "status": self.request.GET.get("status", ""),
        }

        data, _ = get_gov_users(request, params)

        user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
        super_user = is_super_user(user)

        statuses = [
            Option(option["key"], option["value"])
            for option in [
                {"key": "active", "value": UserStatuses.ACTIVE},
                {"key": "deactivated", "value": UserStatuses.DEACTIVATED},
                {"key": "", "value": "All"},
            ]
        ]

        filters = FiltersBar(
            [
                Select(name="status", title="status", options=statuses),
                TextInput(name="email", title="email"),
            ]
        )

        context = {
            "data": data,
            "super_user": super_user,
            "filters": filters,
        }
        return render(request, "users/index.html", context)


class AddUser(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_user_form(request)
        self.action = post_gov_users

    def get_success_url(self):
        messages.success(self.request, UsersPage.INVITE_SUCCESSFUL_BANNER)
        return reverse("users:users")


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_gov_user(request, str(kwargs["pk"]))
        request_user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
        super_user = is_super_user(request_user)
        can_deactivate = not is_super_user(data)
        can_edit_role = data["user"]["id"] != request.session["lite_api_user_id"]

        context = {
            "data": data,
            "super_user": super_user,
            "super_user_role_id": SUPER_USER_ROLE_ID,
            "can_deactivate": can_deactivate,
            "can_edit_role": can_edit_role,
        }
        return render(request, "users/profile.html", context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        return redirect(reverse_lazy("users:user", kwargs={"pk": request.session["lite_api_user_id"]}))


class EditUser(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        user, _ = get_gov_user(request, self.object_pk)
        self.user = user["user"]
        can_edit_role = self.user["id"] != request.session["lite_api_user_id"]
        self.form = edit_user_form(request, self.user, can_edit_role)
        self.data = self.user
        self.action = put_gov_user
        self.success_url = reverse("users:user", kwargs={"pk": self.object_pk})

    def post_success_step(self):
        super().post_success_step()

        # If user is updating their own default_queue, update the local user instance
        if self.user["id"] == self.request.session["lite_api_user_id"]:
            self.request.session["default_queue"] = self.get_validated_data().get("gov_user").get("default_queue")


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = strings.UpdateUser.Status.DEACTIVATE_WARNING

        if status == "reactivate":
            description = strings.UpdateUser.Status.REACTIVATE_WARNING

        context = {
            "title": "Are you sure you want to {} this flag?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "users/change-status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_gov_user(request, str(kwargs["pk"]), json={"status": request.POST["status"]})

        return redirect("/users/")
