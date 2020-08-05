from django.urls import path

from spire import views


app_name = "spire"

urlpatterns = [
    path("application/", views.SpireApplicationSearch.as_view(), name="application-search"),
    path("licence/", views.SpireLicenseSearch.as_view(), name="licence-search"),
    path("licence/<str:id>/", views.SpireLicenceDetail.as_view(), name="licence-detail"),
    path("application/<str:id>/", views.SpireApplicationDetail.as_view(), name="application-detail"),
    path("document/<str:id>/", views.SpireApplicationDocumentDetail.as_view(), name="document-detail"),
]
