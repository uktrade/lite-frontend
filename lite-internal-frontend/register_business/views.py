import json

import requests
from django.shortcuts import render

from conf.settings import env
from register_business import forms


def register(request):
    if request.method == 'POST':
        data = {}

        # Add body fields to data
        for key, value in request.POST.items():
            if key != "button":
                data[key] = value

        # Post it to API
        response = requests.post(env("LITE_API_URL") + '/organisations/',
                                 json=data)

        response_data = json.loads(response.text)

        # If there are errors returned from LITE API, return and show them
        if 'errors' in response_data:
            context = {
                'title': forms.section1.forms[0].title,
                'page': forms.section1.forms[0],
                'errors': response_data['errors'],
                'data': data
            }
            return render(request, 'register_business/form.html', context)
        context = {'name': response_data['organisation']['name']}
        return render(request, 'register_business/registration_success.html', context)

    elif request.method == 'GET':
        context = {
            'page': forms.section1.forms[0],
            'title': forms.section1.forms[0].title,
        }
        return render(request, 'register_business/form.html', context)
