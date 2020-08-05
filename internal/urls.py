from django.urls import path

from django.http import HttpResponse


app_name = 'internal'


urlpatterns = [
    path('', lambda request: HttpResponse('internal app'))
]
