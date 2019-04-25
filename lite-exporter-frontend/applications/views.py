from django.http import HttpResponse
from django.shortcuts import render

from applications.services import get_applications, get_application


def index(request):
    data, status_code = get_applications(request)

    if status_code is not 200:
        raise HttpResponse(status=status_code)

    context = {
        'data': data,
        'title': 'Applications',
    }
    return render(request, 'applications/index.html', context)


def application(request, pk):
    data, status_code = get_application(request, str(pk))

    if status_code is not 200:
        raise HttpResponse(status=status_code)

    context = {
        'data': data,
        'title': data.get("application").get("name"),
    }
    return render(request, 'applications/application.html', context)
