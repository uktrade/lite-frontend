import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/')

    context = {
        'title': 'Drafts',
        'data': response.json(),
        'applicationDeleted': request.GET.get('application_deleted')
    }
    return render(request, 'drafts/index.html', context)
