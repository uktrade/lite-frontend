import requests

from django.shortcuts import render

from conf.settings import env


def organisations(request):
    response = requests.get(env("LITE_API_URL") + '/organisations')
    context = {
        'data': response.json(),
        'title': 'Organisations',
    }
    return render(request, 'organisations/index.html', context)
