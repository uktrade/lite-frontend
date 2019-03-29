import libraries.jsondate as json

import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    context = {
        'title': 'Licences',
    }
    return render(request, 'licences/index.html', context)
