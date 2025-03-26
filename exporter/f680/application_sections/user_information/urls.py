from django.urls import path

from . import views


app_name = "user_information"

urlpatterns = [
    path("add-item/", views.UserInformationView.as_view(), name="wizard"),
    path("edit-item/<uuid:id>/", views.UserInformationView.as_view(), name="wizard"),
    path("remove/<uuid:entity_to_remove_id>/", views.UserInformationRemoveEntityView.as_view(), name="remove"),
    path("summary/", views.UserInformationSummaryView.as_view(), name="summary"),
]
