from django.urls import path

from . import views


app_name = "f680"

urlpatterns = [
    path("apply/", views.F680ApplicationCreateView.as_view(), name="apply"),  # PS-IGNORE
]
