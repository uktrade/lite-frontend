from django.shortcuts import render

from django.urls import reverse_lazy

from django.shortcuts import render
from django.urls import reverse_lazy

from core.helpers import Section, Tile


def hub(request):
    context = {
        'title': 'Department of International Trade Hub',
        'sections': [
            Section("", "", [
                Tile("Manage Organisations", "Manage Organisations ", "/organisations"),
            ]),
        ],
    }
    return render(request, 'core/hub.html', context)


def signin(request):
    context = {
        'title': 'Sign in',
    }
    return render(request, 'core/signin.html', context)


def signout(request):
    context = {
        'title': 'Sign out',
    }
    return render(request, 'core/signout.html', context)


def placeholder(request):
    context = {
        'title': 'Placeholder',
    }
    return render(request, 'core/placeholder.html', context)
