from teams.services import get_team, get_teams, \
    post_teams, update_team, get_users_by_team
from teams import forms

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users.services import get_gov_user


class Team(TemplateView):
    def get(self, request, **kwargs):
        """
        View the user's team
        """
        user, status_code = get_gov_user(request)
        team, status_code = get_team(request, user['user']['team']['id'])
        users, status_code = get_users_by_team(request, team['team']['id'])

        context = {
            'team': team['team'],
            'title': 'Users - ' + team['team']['name'],
            'users': users['users'],
        }
        return render(request, 'teams/own_team.html', context)


class TeamsList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_teams(request)

        context = {
            'data': data,
            'title': 'Teams',
        }
        return render(request, 'teams/index.html', context)


class AddTeam(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Team',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_teams(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add Team',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('teams:teams'))


class TeamDetail(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_team(request, str(kwargs['pk']))
        title = data['team']['name']
        data, status_code = get_users_by_team(request, str(kwargs['pk']))
        context = {
            'title': title,
            'users': data['users'],
        }
        return render(request, 'teams/team.html', context)


class EditTeam(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_team(request, str(kwargs['pk']))
        context = {
            'data': data.get('team'),
            'title': 'Edit Team',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_team(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add Team',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('teams:teams'))
