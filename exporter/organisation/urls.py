from django.urls import path, include

from exporter.organisation import views

app_name = "organisation"

urlpatterns = [
    path("", views.RedirectToMembers.as_view(), name="organisation"),
    path("members/", include("exporter.organisation.members.urls")),
    path("sites/", include("exporter.organisation.sites.urls")),
    path("roles/", include("exporter.organisation.roles.urls")),
    path("details/", views.Details.as_view(), name="details"),
    path("document/<uuid:pk>/", views.DocumentOnOrganisation.as_view(), name="document"),
    path(
        "upload/firearms-certificate/",
        views.UploadFirearmsCertificate.as_view(),
        name="upload-firearms-certificate",
    ),
    path(
        "upload/section-five-certificate/",
        views.UploadSectionFiveCertificate.as_view(),
        name="upload-section-five-certificate",
    ),
]
