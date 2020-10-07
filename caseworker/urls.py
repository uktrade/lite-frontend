from django.conf import settings
from django.urls import include, path

import caseworker.core.views


urlpatterns = [
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
    path("search/", include("caseworker.search.urls")),
]


if settings.FEATURE_SPIRE_SEARCH_ON:
    urlpatterns.append(path("spire/", include("caseworker.spire.urls")))
    urlpatterns.append(path("spire-dms/", include("caseworker.spire_dms.urls")))


if settings.FEATURE_DEBUG_TOOLBAR_ON:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns


handler403 = caseworker.core.views.handler403
handler404 = caseworker.core.views.handler404
handler500 = caseworker.core.views.handler500
