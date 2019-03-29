from django.shortcuts import render
from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from core.helpers import Section, Tile


def hub(request):
    context = {
        'title': get_string('EXPORTER_HUB_TITLE'),
        'sections': [
            Section("", "", [
                Tile(get_string('APPLY_FOR_A_LICENCE'), "", reverse_lazy('new_application:index')),
            ]),
            Section("Manage", "", [
                Tile(get_string('DRAFTS'), "", reverse_lazy('drafts:drafts')),
                Tile(get_string('APPLICATIONS'), "", reverse_lazy('applications:applications')),
            ]),
        ],
        'applicationDeleted': request.GET.get('application_deleted')
    }
    return render(request, 'core/hub.html', context)


def signin(request):
    context = {
        'title': get_string('SIGN_IN'),
    }
    return render(request, 'core/signin.html', context)


def signout(request):
    context = {
        'title': get_string('SIGNED_OUT'),
    }
    return render(request, 'core/signout.html', context)


def placeholder(request):
    context = {
        'title': 'Placeholder',
    }
    return render(request, 'core/placeholder.html', context)
