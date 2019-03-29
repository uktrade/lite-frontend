from django.urls import path

from . import views

app_name = 'drafts'
urlpatterns = [
    # ex: /
    path('', views.index, name='drafts'),
]
