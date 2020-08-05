from django.urls import path, include

from organisation import views

app_name = "organisation"

urlpatterns = [
    path("", views.RedirectToMembers.as_view(), name="organisation"),
    path("members/", include("organisation.members.urls")),
    path("sites/", include("organisation.sites.urls")),
    path("roles/", include("organisation.roles.urls")),
    path("details/", views.Details.as_view(), name="details"),
]
