from django.urls import path

from exporter.core import views
from exporter.core.organisation.views import Registration, SelectOrganisation


app_name = "core"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("select-organisation/", SelectOrganisation.as_view(), name="select_organisation"),
    path(
        "register-an-organisation/",
        Registration.as_view(),
        name="register_an_organisation_triage",
    ),
    path(
        "register-an-organisation/confirm/",
        views.RegisterAnOrganisationConfirmation.as_view(),
        name="register_an_organisation_confirm",
    ),
    path("signature-help/", views.SignatureHelp.as_view(), name="signature_help"),
    path("certificate/", views.CertificateDownload.as_view(), name="certificate"),
    path("register-name/", views.RegisterName.as_view(), name="register_name"),
    path("privacy-notice/", views.PrivacyNotice.as_view(), name="privacy_notice"),
]
