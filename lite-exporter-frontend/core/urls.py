from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pick-organisation/", views.PickOrganisation.as_view(), name="pick_organisation"),
    path(
        "register-an-organisation/",
        views.RegisterAnOrganisationTriage.as_view(),
        name="register_an_organisation_triage",
    ),
    path(
        "register-an-organisation/confirm/",
        views.RegisterAnOrganisationConfirmation.as_view(),
        name="register_an_organisation_confirm",
    ),
    path(
        "register-an-organisation/<str:type>/<str:location>/",
        views.RegisterAnOrganisation.as_view(),
        name="register_an_organisation",
    ),
]
