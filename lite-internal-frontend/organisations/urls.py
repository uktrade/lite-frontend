from django.urls import path

from . import views

app_name = 'organisations'
urlpatterns = [
    path('', views.show_orgs, name='organisations'),
]
