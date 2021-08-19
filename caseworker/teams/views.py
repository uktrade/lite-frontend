from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView

from lite_content.lite_internal_frontend.teams import TeamsPage
from lite_forms.views import SingleFormView

from caseworker.core.constants import Permission
from caseworker.core.services import get_user_permissions
from caseworker.teams.forms import add_team_form, edit_team_form
from caseworker.teams.services import get_team, get_teams, post_teams, get_users_by_team, put_team
from caseworker.users.services import get_gov_user
from caseworker.auth.views import CaseworkerLoginRequiredMixin


class TeamsList(CaseworkerLoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        data = get_teams(request)

        context = {
            "data": data,
        }
        return render(request, "teams/index.html", context)


class Team(CaseworkerLoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        user, _ = get_gov_user(self.request)
        return reverse_lazy("teams:team", kwargs={"pk": user["user"]["team"]["id"]})


class TeamDetail(CaseworkerLoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user, _ = get_gov_user(self.request)
        team, _ = get_team(request, str(kwargs["pk"]))
        users, _ = get_users_by_team(request, str(kwargs["pk"]))

        context = {
            "team": team["team"],
            "users": users["users"],
            "is_user_in_team": user["user"]["team"]["id"] == team["team"]["id"],
            "can_manage_picklists": Permission.MANAGE_PICKLISTS.value in get_user_permissions(request),
        }
        return render(request, "teams/team.html", context)


class AddTeam(CaseworkerLoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_team_form()
        self.action = post_teams

    def get_success_url(self):
        messages.success(self.request, TeamsPage.SUCCESS_MESSAGE)
        return reverse("teams:teams")


class EditTeam(CaseworkerLoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        team, _ = get_team(request, self.object_pk)
        self.form = edit_team_form()
        self.data = team["team"]
        self.action = put_team
        self.success_url = reverse("teams:teams")
