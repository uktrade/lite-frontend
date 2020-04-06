from django.urls import path

from . import views

app_name = "licences"
urlpatterns = [
    path("", views.ApplicationsList.as_view(), name="licences"),
]
