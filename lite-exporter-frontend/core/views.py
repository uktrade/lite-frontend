import requests
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from conf.settings import env
from core.builtins.custom_tags import get_string
from core.helpers import Section, Tile
from core.models import User


@login_required
def hub(request):
    context = {
        'title': get_string('hub.title'),
        'sections': [
            Section("", "", [
                Tile(get_string('licences.apply_for_a_licence'), "",
                     reverse_lazy('apply_for_a_licence:index')),
            ]),
            Section("Manage", "", [
                Tile(get_string('drafts.title'), "",
                     reverse_lazy('drafts:drafts')),
                Tile(get_string('applications.title'), "",
                     reverse_lazy('applications:applications')),
                Tile('Goods', "", reverse_lazy('goods:goods')),
                Tile('Sites', "", reverse_lazy('sites:sites')),
                Tile('Users', "", reverse_lazy('users:users')),
            ]),
        ],
        'applicationDeleted': request.GET.get('application_deleted'),
    }
    return render(request, 'core/hub.html', context)


def login(request):
    if request.method == 'GET':
        context = {
            'title': get_string('misc.sign_in'),
        }
        return render(request, 'core/login.html', context)

    if request.method == 'POST':
        response = requests.post(env('LITE_API_URL') + '/users/authenticate/',
                                 json={
                                     'email': request.POST.get('email'),
                                     'password': request.POST.get('password'),
                                 },
                                 )

        # If login isn't successful, return previous page
        if response.status_code is not 200:
            context = {
                'title': get_string('misc.sign_in'),
                'error': True,
                'email': request.POST.get('email'),
            }
            return render(request, 'core/login.html', context)

        user_data = response.json().get('user')

        user_object, created = User.objects.get_or_create(
            id=user_data.get('id'), defaults={
                'email': user_data.get('email'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
        })

        django_login(request, user=user_object)

        # Redirect to index page as a signed in user
        return redirect('/')


def logout(request):
    django_logout(request)

    context = {
        'title': get_string('misc.signed_out'),
    }
    return render(request, 'core/loggedout.html', context)
