from django.urls import path

from caseworker.flags import views

app_name = "flags"

urlpatterns = [
    path("", views.FlagsList.as_view(), name="flags"),
]
