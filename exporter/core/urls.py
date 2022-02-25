from django.urls import path

from exporter.core import views

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
    path("signature-help/", views.SignatureHelp.as_view(), name="signature_help"),
    path("certificate/", views.CertificateDownload.as_view(), name="certificate"),
    path("register-name/", views.RegisterName.as_view(), name="register_name"),
]
