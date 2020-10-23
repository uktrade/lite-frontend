from django.conf import settings
from django.urls import include, path

import exporter.core.views


urlpatterns = [
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
    path("goods/", include("exporter.goods.urls")),
    path("licences/", include("exporter.licences.urls")),
    path("organisation/", include("exporter.organisation.urls")),
    path("ecju-queries/", include("exporter.ecju_queries.urls")),
    path("", include("exporter.hmrc.urls")),
]

handler403 = exporter.core.views.handler403

if settings.FEATURE_DEBUG_TOOLBAR_ON:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
