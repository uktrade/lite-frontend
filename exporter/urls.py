from django.urls import include, path

urlpatterns = [
    path("", include("exporter.core.urls")),
    path("applications/", include("exporter.applications.urls")),
    path("apply-for-a-licence/", include("exporter.apply_for_a_licence.urls")),
    path("auth/", include("exporter.auth.urls")),
    path("compliance/", include("exporter.compliance.urls")),
    path("end-users/", include("exporter.end_users.urls")),
    path("goods/", include("exporter.goods.urls")),
    path("licences/", include("exporter.licences.urls")),
    path("organisation/", include("exporter.organisation.urls")),
    path("ecju-queries/", include("exporter.ecju_queries.urls")),
    path("", include("exporter.hmrc.urls")),
]

handler403 = "exporter.conf.views.handler403"
