from django.urls import path

from . import views

app_name = "licences"
urlpatterns = [
    path("", views.Licences.as_view(), name="licences"),
    path("<uuid:pk>/", views.Licence.as_view(), name="licence"),
]
