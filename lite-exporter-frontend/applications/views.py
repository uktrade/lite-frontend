import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    response = requests.get(env("LITE_API_URL") + '/applications/')

    context = {
        'data': response.json(),
        'title': 'Applications',
    }
    return render(request, 'applications/index.html', context)


def application(request, id):
    response = requests.get(env("LITE_API_URL") + '/applications/' + str(id) + '/')

    context = {
        'data': response.json(),
        'title': response.json().get("application").get("name"),
    }
    return render(request, 'applications/application.html', context)
