from django.conf import settings
from django.urls import include, path

import caseworker.core.views

from core.accessibility.views import CaseworkerAccessibilityStatementView


urlpatterns = [
    path("healthcheck/", include("health_check.urls")),
    path("", include("caseworker.core.urls")),
    path("auth/", include("caseworker.auth.urls")),
    path("queues/<uuid:queue_pk>/cases/<uuid:pk>/", include("caseworker.cases.urls")),
    path("flags/", include("caseworker.flags.urls")),
    path("document-templates/", include("caseworker.letter_templates.urls")),
    path("open-general-licences/", include("caseworker.open_general_licences.urls")),
    path("organisations/", include("caseworker.organisations.urls")),
    path("queues/", include("caseworker.queues.urls")),
    path("team/picklists/", include("caseworker.picklists.urls")),
    path("team", include("caseworker.teams.urls")),
    path("users/", include("caseworker.users.urls")),
    path("routing-rules/", include("caseworker.routing_rules.urls")),
    path("compliance/", include("caseworker.compliance.urls")),
    path("api/", include("core.api.urls")),  # proxies for lite-api views. used by frontend javascript
    path("", include("caseworker.external_data.urls")),
    path("feedback/", include("core.feedback.urls")),
    path("cookies/", include("core.cookies.urls")),
    path("tau/", include("caseworker.tau.urls")),
    path("tau/report_summary/", include("caseworker.report_summary.urls")),
    path("search/", include("caseworker.search.urls")),
    path("bookmarks/", include("caseworker.bookmarks.urls")),
    path(
        "accessibility-statement/",
        CaseworkerAccessibilityStatementView.as_view(),
        name="caseworker-accessibility-statement",
    ),
]


if settings.MOCK_SSO_ACTIVATE_ENDPOINTS:
    urlpatterns = [
        path("", include("caseworker.mock_sso.urls")),
    ] + urlpatterns


if settings.FEATURE_DEBUG_TOOLBAR_ON:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns


handler403 = caseworker.core.views.handler403
handler404 = caseworker.core.views.handler404
handler500 = caseworker.core.views.handler500
