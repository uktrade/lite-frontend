from django.urls import path

from caseworker.flags.views import AssignFlags
from caseworker.organisations import views

from caseworker.organisations.members.users.views import AddExporterAdminView

app_name = "organisations"

urlpatterns = [
    path("", views.OrganisationList.as_view(), name="organisations"),
    path("<uuid:pk>/", views.OrganisationDetails.as_view(), name="organisation"),
    path("<uuid:pk>/review/", views.OrganisationReview.as_view(), name="organisation_review"),
    path("<uuid:pk>/members/", views.OrganisationMembers.as_view(), name="organisation_members"),
    path("<uuid:pk>/sites/", views.OrganisationSites.as_view(), name="organisation_sites"),
    path("<uuid:pk>/assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path("register/", views.RegisterOrganisation.as_view(), name="register"),
    path("<uuid:pk>/edit/", views.EditOrganisation.as_view(), name="edit"),
    path("<uuid:pk>/edit-address/", views.EditOrganisationAddress.as_view(), name="edit-address"),
    path("register-hmrc/", views.RegisterHMRC.as_view(), name="register_hmrc"),
    path("<uuid:pk>/add-exporter-admin/", AddExporterAdminView.as_view(), name="add-exporter-admin"),
]
