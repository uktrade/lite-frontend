from django.conf import settings
from django.urls import include, path

from caseworker.conf import views


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
]


if settings.FEATURE_SPIRE_SEARCH_ON:
    urlpatterns.append(path("spire/", include("caseworker.spire.urls")))


handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500
