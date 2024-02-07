from django.conf import settings
from django.urls import include, path

import exporter.core.views

from core.accessibility.views import ExporterAccessibilityStatementView


urlpatterns = [
    path("healthcheck/", include("health_check.urls")),
    path("", include("exporter.core.urls")),
    path("applications/", include("exporter.applications.urls")),
    path("apply-for-a-licence/", include("exporter.apply_for_a_licence.urls")),
    path("auth/", include("exporter.auth.urls")),
]

if not settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
    urlpatterns += [
        path("compliance/", include("exporter.compliance.urls")),
    ]

urlpatterns += [
    path("end-users/", include("exporter.end_users.urls")),
    path("product-list/", include("exporter.goods.urls")),
    path("licences/", include("exporter.licences.urls")),
    path("organisation/", include("exporter.organisation.urls")),
    path("ecju-queries/", include("exporter.ecju_queries.urls"), name="ecju-queries"),
    path("", include("exporter.hmrc.urls")),
    path("feedback/", include("core.feedback.urls")),
    path("cookies/", include("core.cookies.urls")),
    path(
        "accessibility-statement/",
        ExporterAccessibilityStatementView.as_view(),
        name="exporter-accessibility-statement",
    ),
]

if settings.MOCK_SSO_ACTIVATE_ENDPOINTS:
    urlpatterns = [
        path("", include("exporter.mock_sso.urls")),
    ] + urlpatterns

handler403 = exporter.core.views.handler403

if settings.FEATURE_DEBUG_TOOLBAR_ON:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
