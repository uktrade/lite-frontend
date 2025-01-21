from django.urls import path

from . import views


app_name = "f680"

urlpatterns = [
    path("apply/", views.ApplyView.as_view(), name="apply"),
]
