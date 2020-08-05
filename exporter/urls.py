from django.urls import path

from django.http import HttpResponse


app_name = 'exporter'


urlpatterns = [
    path('', lambda request: HttpResponse('exporter app'))
]
