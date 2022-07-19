from django.urls import path
from django.conf import settings

from exporter.core import views
from exporter.core.organisation.views import (
    Registration,
    SelectOrganisation,
    DraftConfirmation,
    OrganisationEditField,
)


app_name = "core"

if settings.FEATURE_FLAG_DJANGO_FORMS_REGISTRATION_ENABLED:
    registration_patterns = [
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
        path(
            "register-an-organisation/draft-confirmation/",
            DraftConfirmation.as_view(),
            name="register_draft_confirm",
        ),
        path(
            "register-an-organisation/edit/<str:field>/",
            OrganisationEditField.as_view(),
            name="register_draft_edit",
        ),
    ]

else:
    registration_patterns = [
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

urlpatterns = (
    [
        path("", views.Home.as_view(), name="home"),
        path("select-organisation/", SelectOrganisation.as_view(), name="select_organisation"),
    ]
    + registration_patterns
    + [
        path("signature-help/", views.SignatureHelp.as_view(), name="signature_help"),
        path("certificate/", views.CertificateDownload.as_view(), name="certificate"),
        path("register-name/", views.RegisterName.as_view(), name="register_name"),
    ]
)
