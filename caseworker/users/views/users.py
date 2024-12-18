from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from caseworker.cases.services import update_mentions

from core.auth.views import LoginRequiredMixin
from caseworker.core.constants import (
    UserStatuses,
)
from lite_content.lite_internal_frontend import strings
from lite_forms.components import FiltersBar, Select, Option, TextInput
from caseworker.users.services import (
    get_gov_users,
    put_gov_user,
    get_gov_user,
    is_super_user,
    get_user_case_note_mentions,
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


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_gov_user(request, str(kwargs["pk"]))
        context = {
            "data": data,
        }
        return render(request, "users/profile.html", context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        return redirect(reverse_lazy("users:user", kwargs={"pk": request.session["lite_api_user_id"]}))


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


class UserCaseNoteMentions(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        self.params = {"page": int(self.request.GET.get("page", 1))}

        my_unread_mentions = [
            {"id": m["id"], "is_accessed": True}
            for m in self.mentions.get("results", [])
            if not m["is_accessed"] and m["user"]["id"]
        ]
        if my_unread_mentions:
            update_mentions(request, my_unread_mentions)
        return render(request, "users/mentions.html", {"data": self.mentions})

    @cached_property
    def mentions(self):
        data, _ = get_user_case_note_mentions(self.request, self.params)
        return data
