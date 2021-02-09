from django.urls import path, include

from exporter.organisation import views

app_name = "organisation"

urlpatterns = [
    path("", views.RedirectToMembers.as_view(), name="organisation"),
    path("members/", include("exporter.organisation.members.urls")),
    path("sites/", include("exporter.organisation.sites.urls")),
    path("roles/", include("exporter.organisation.roles.urls")),
    path("details/", views.Details.as_view(), name="details"),
]
