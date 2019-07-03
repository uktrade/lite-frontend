from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from libraries.forms.generators import form_page
from teams.services import get_teams
from users.forms import add_user_form, edit_user_form
from users.services import get_gov_users, post_gov_users, put_gov_user, get_gov_user


class UsersList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_gov_users(request)

        context = {
            'data': data,
            'title': 'Users',
        }
        return render(request, 'users/index.html', context)


class AddUser(TemplateView):
    def get(self, request, **kwargs):
        teams = get_teams(request, True)
        return form_page(request, add_user_form(teams))

    def post(self, request, **kwargs):
        response, status_code = post_gov_users(request, request.POST)
        teams = get_teams(request, True)
        if status_code != 201:
            return form_page(request, add_user_form(teams), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('users:users'))


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_gov_user(request, str(kwargs['pk']))
        user = data.get('user')

        context = {
            'data': data,
            'title': user.get('first_name') + ' ' + user.get('last_name')
        }
        return render(request, 'users/profile.html', context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        user = request.user
        return redirect(reverse_lazy('users:user', kwargs={'pk': user.id}))


class EditUser(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_gov_user(request, str(kwargs['pk']))
        teams = get_teams(request, True)
        return form_page(request, edit_user_form(teams), data=data)

    def post(self, request, **kwargs):
        response, status_code = put_gov_user(request, str(kwargs['pk']), request.POST)
        teams = get_teams(request, True)
        if status_code != 200:
            return form_page(request, edit_user_form(teams), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('users:users'))


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs['status']
        description = ''

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        if status == 'deactivate':
            description = get_string('update_user.status.deactivate_warning')

        if status == 'reactivate':
            description = get_string('update_user.status.reactivate_warning')

        context = {
            'title': 'Are you sure you want to {} this flag?'.format(status),
            'description': description,
            'user_id': str(kwargs['pk']),
            'status': status,
        }
        return render(request, 'users/change_status.html', context)

    def post(self, request, **kwargs):
        status = kwargs['status']

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        put_gov_user(request, str(kwargs['pk']), json={'status': request.POST['status']})

        return redirect('/users/')
