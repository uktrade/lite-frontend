from django.urls import path

from compliance import views

app_name = "compliance"

urlpatterns = [
    path(
        "open-licence-returns/<uuid:pk>/download/",
        views.AnnualReturnsDownload.as_view(),
        name="open_licence_returns_download",
    ),
]
