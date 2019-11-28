from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("applications/", include("applications.urls")),
    path("apply-for-a-licence/", include("apply_for_a_licence.urls")),
    path("auth/", include("auth.urls", namespace="authbroker")),
    path("end-users/", include("end_users.urls")),
    path("goods/", include("goods.urls")),
    path("licences/", include("licences.urls")),
    path("sites/", include("sites.urls")),
    path("users/", include("users.urls")),
    path("roles/", include("roles.urls")),
    path("", include("hmrc.urls")),
]
