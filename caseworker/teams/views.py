from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView, FormView

from caseworker.core.constants import Permission
from caseworker.core.services import get_user_permissions
from lite_content.lite_internal_frontend.teams import TeamsPage
from lite_forms.views import SingleFormView
from caseworker.teams.forms import add_team_form, EditTeamForm
from caseworker.teams.services import get_team, get_teams, post_teams, get_users_by_team, put_team
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin


class TeamsList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        data = get_teams(request)

        context = {
            "data": data,
        }
        return render(request, "teams/index.html", context)


class Team(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        user, _ = get_gov_user(self.request)  # noqa: F811
        return reverse_lazy("teams:team", kwargs={"pk": user["user"]["team"]["id"]})


class TeamDetail(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        user, _ = get_gov_user(self.request)  # noqa: F811
        team, _ = get_team(request, str(kwargs["pk"]))  # noqa: F811
        users, _ = get_users_by_team(request, str(kwargs["pk"]))  # noqa: F811

        context = {
            "team": team["team"],
            "users": users["users"],
            "is_user_in_team": user["user"]["team"]["id"] == team["team"]["id"],
            "can_manage_picklists": Permission.MANAGE_PICKLISTS.value in get_user_permissions(request),
        }
        return render(request, "teams/team.html", context)


class AddTeam(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_team_form()
        self.action = post_teams

    def get_success_url(self):
        messages.success(self.request, TeamsPage.SUCCESS_MESSAGE)
        return reverse("teams:teams")


class EditTeam(LoginRequiredMixin, FormView):
    template_name = "teams/team-edit.html"
    form_class = EditTeamForm
    success_url = reverse_lazy("teams:teams")

    def get_initial(self):
        self.object_pk = self.kwargs["pk"]
        team, _ = get_team(self.request, self.object_pk)  # noqa: F811
        part_of_ecju = team["team"]["part_of_ecju"]
        is_ogd = team["team"]["is_ogd"]

        initial = super().get_initial()
        initial["name"] = team["team"]["name"]
        initial["part_of_ecju"] = part_of_ecju
        initial["is_ogd"] = is_ogd

        return initial

    def form_valid(self, form):
        data_dict = form.cleaned_data

        data_dict["part_of_ecju"] = (False, True)[data_dict["part_of_ecju"] == "True"]
        data_dict["is_ogd"] = (False, True)[data_dict["is_ogd"] == "True"]

        data_json, _ = put_team(self.request, self.kwargs["pk"], data_dict)  # noqa: F811
        errors = data_json.get("errors", {})

        for field_name, field_errors in errors.items():
            if field_name not in form.fields:
                form.add_error(None, field_errors)
                continue
            for field_error in field_errors:
                form.add_error(field_name, field_error)

        return super().form_valid(form)
