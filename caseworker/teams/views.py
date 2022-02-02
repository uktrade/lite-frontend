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

from django.contrib import messages
from django.utils.translation import gettext as _

class TeamsList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        data = get_teams(request)

        context = {
            "data": data,
        }
        return render(request, "teams/index.html", context)


class Team(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        user, _ = get_gov_user(self.request)
        return reverse_lazy("teams:team", kwargs={"pk": user["user"]["team"]["id"]})


class TeamDetail(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
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

    def get_form(self, *args, **kwargs):
        self.object_pk = self.kwargs["pk"]
        team, _ = get_team(self.request, self.object_pk)
        part_of_ecju = team["team"]["part_of_ecju"]
        is_ogd = team["team"]["is_ogd"]
        form = super().get_form(*args, **kwargs)
       
        form.fields['name'].initial = team["team"]["name"]
        form.fields['part_of_ecju'].initial = True if part_of_ecju == True else False
        form.fields['is_ogd'].initial = True if is_ogd == True else False
        
        return form

    def post(self, *args, **kwargs):
        form = EditTeamForm(self.request.POST)
        data_dict = self.request.POST.dict()
        if form.is_valid():
            response = put_team(self.request, self.kwargs["pk"], data_dict)
            status_code = response[-1]
            data_json = response[0]
            print(response)
            print(self.kwargs["pk"])
            errors = data_json.get("errors", {})
            for field_name, field_errors in errors.items():
                if field_name not in form.fields:
                    form.add_error(None, field_errors)
                    continue
                for field_error in field_errors:
                    form.add_error(field_name, field_error)

        return super().post(*args, **kwargs)