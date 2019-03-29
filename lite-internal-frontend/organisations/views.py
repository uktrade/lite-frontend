import requests

from django.shortcuts import render

import libraries.jsondate as jsondate

from conf.settings import env


def show_orgs(request):
    response = requests.get(env("LITE_API_URL") + '/organisations')
    context = {
        'data': jsondate.loads(response.text),
        'title': 'Organisations',
    }
    return render(request, 'organisations/index.html', context)
