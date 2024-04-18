from django.urls import path

from caseworker.external_data import views

app_name = "external_data"

urlpatterns = [
    path(
        "denials/add-by-csv/", views.DenialUploadView.as_view(), name="denials-add-by-csv"
    ),  # TODO: rename back to "denials/upload/" and "denials-upload" when we are ready to release this to users
    path("denials/<uuid:pk>/", views.DenialDetailView.as_view(), name="denial-detail"),
    path("denials/<uuid:pk>/revoke/", views.DenialRevokeView.as_view(), name="denial-revoke"),
]
