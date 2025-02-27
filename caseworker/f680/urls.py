from django.urls import include, path

from caseworker.f680 import views


app_name = "f680"

urlpatterns = [
    path(
        "",
        views.CaseDetailView.as_view(),
        name="details",
    ),
    path("document/", include("caseworker.f680.document.urls")),
]
