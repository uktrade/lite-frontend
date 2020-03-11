from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from core.services import get_organisation_user, put_organisation_user, get_organisation_users
from lite_forms.components import Option, FiltersBar, Select
from lite_forms.views import SingleFormView
from organisation.members.forms import add_user_form, edit_user_form, assign_sites
from organisation.members.services import post_users, get_user, is_super_user
from organisation.sites.services import put_assign_sites
from organisation.views import OrganisationView


class Members(OrganisationView):
    template_name = "members/index"

    def get_additional_context(self):
        status = self.request.GET.get("status", "active")
        params = {"page": int(self.request.GET.get("page", 1)), "status": status}
        data, _ = get_organisation_users(self.request, str(self.request.user.organisation), params)
        statuses = [
            Option(option["key"], option["value"])
            for option in [{"key": "active", "value": "Active"}, {"key": "", "value": "All"}]
        ]
        filters = FiltersBar([Select(name="status", title="status", options=statuses)])

        return {
            "status": status,
            "data": data,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "filters": filters,
        }


class AddUser(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_user_form(request)
        self.success_url = reverse_lazy("organisation:members:members")
        self.action = post_users


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        request_user = get_organisation_user(request, str(request.user.organisation), str(kwargs["pk"]))
        user = get_user(request)
        is_request_user_super_user = is_super_user(request_user)
        is_user_super_user = is_super_user(user)
        is_self_editing = user["id"] == request_user["id"]

        show_change_status = not is_self_editing and is_user_super_user and not is_request_user_super_user
        show_change_role = not is_self_editing and is_user_super_user
        show_assign_sites = not is_self_editing and not is_request_user_super_user

        context = {
            "signed_in_user": user,
            "profile": request_user,
            "show_change_status": show_change_status,
            "show_change_role": show_change_role,
            "show_assign_sites": show_assign_sites,
        }
        return render(request, "organisation/members/profile.html", context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        user = request.user
        return redirect(reverse_lazy("organisation:members:user", kwargs={"pk": user.lite_api_user_id}))


class EditUser(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        user = get_organisation_user(request, str(request.user.organisation), str(self.object_pk))
        can_edit_role = user["id"] != request.user.lite_api_user_id
        self.form = edit_user_form(request, self.object_pk, can_edit_role)
        self.data = user
        self.action = put_organisation_user
        self.success_url = reverse_lazy("organisation:members:user", kwargs={"pk": self.object_pk})


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = (
                "This member will no longer be able to log in or perform tasks on LITE on behalf of your organisation."
            )

        if status == "reactivate":
            description = (
                "This member will be able to log in to and perform tasks on LITE on behalf of your organisation."
            )

        context = {
            "title": "Are you sure you want to {} this user?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "organisation/members/change-status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_organisation_user(request, str(kwargs["pk"]), request.POST)

        return redirect(reverse_lazy("organisation:members:user", kwargs={"pk": kwargs["pk"]}))


class AssignSites(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_user(request, self.object_pk)
        self.form = assign_sites(request)
        self.action = put_assign_sites
        self.success_url = reverse_lazy("organisation:members:user", kwargs={"pk": self.object_pk})
