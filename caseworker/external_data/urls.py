from django.urls import path

from caseworker.external_data import views

app_name = "external_data"

urlpatterns = [
    path("denials/upload/", views.DenialUploadView.as_view(), name="denials-upload"),
    path("denials/upload/<uuid:pk>/", views.DenialDetailView.as_view(), name="denial-detail"),
]
