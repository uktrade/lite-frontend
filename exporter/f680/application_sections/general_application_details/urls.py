from django.urls import path

from . import views


app_name = "general_application_details"

urlpatterns = [
    path("", views.GeneralApplicationDetailsView.as_view(), name="wizard"),
]
