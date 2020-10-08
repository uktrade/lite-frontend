from django.urls import path

from caseworker.spire_dms import views


app_name = "spire_dms"

urlpatterns = [
    path("application/", views.SpireApplicationSearch.as_view(), name="application-search"),
    path("application/<str:id>/", views.SpireApplicationDetail.as_view(), name="application-detail"),
    path("licence/", views.SpireLicenseSearch.as_view(), name="licence-search"),
    path("licence/<str:id>/", views.SpireLicenceDetail.as_view(), name="licence-detail"),
]
