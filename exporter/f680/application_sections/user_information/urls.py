from django.urls import path

from . import views


app_name = "user_information"

urlpatterns = [
    path("add-item/", views.UserInformationView.as_view(), name="wizard"),
    path("edit-item/<uuid:id>/", views.UserInformationView.as_view(), name="wizard"),
]
