from django.urls import path

from . import views

app_name = "licences"
urlpatterns = [
    # ex: /
    path("", views.index, name="licences"),
]
