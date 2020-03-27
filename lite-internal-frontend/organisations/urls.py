from django.urls import path

from flags.views import AssignFlags
from organisations import views

app_name = "organisations"

urlpatterns = [
    path("", views.OrganisationList.as_view(), name="organisations"),
    path("<uuid:pk>/", views.OrganisationDetails.as_view(), name="organisation"),
    path("<uuid:pk>/members/", views.OrganisationMembers.as_view(), name="organisation_members"),
    path("<uuid:pk>/sites/", views.OrganisationSites.as_view(), name="organisation_sites"),
    path("<uuid:pk>/assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path("register/", views.RegisterOrganisation.as_view(), name="register"),
    path("<uuid:pk>/edit/", views.EditOrganisation.as_view(), name="edit"),
    path("register-hmrc/", views.RegisterHMRC.as_view(), name="register_hmrc"),
]
