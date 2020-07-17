from django.contrib import admin
from django.urls import include, path

from conf import views

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls")),
    path("queues/<uuid:queue_pk>/cases/<uuid:pk>/", include("cases.urls")),
    path("flags/", include("flags.urls")),
    path("document-templates/", include("letter_templates.urls")),
    path("open-general-licences/", include("open_general_licences.urls")),
    path("organisations/", include("organisations.urls")),
    path("queues/", include("queues.urls")),
    path("team/picklists/", include("picklists.urls")),
    path("team", include("teams.urls")),
    path("users/", include("users.urls")),
    path("routing-rules/", include("routing_rules.urls")),
    path("compliance/", include("compliance.urls")),
]

handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500
