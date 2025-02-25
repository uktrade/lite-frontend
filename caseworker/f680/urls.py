from django.urls import path

from caseworker.f680 import views

app_name = "f680"

urlpatterns = [
    path(
        "",
        views.CaseDetailView.as_view(),
        name="details",
    ),
    path(
        "generate-document/preview/",
        views.F680PreviewDocument.as_view(),
        name="generate_document_preview",
    ),
    path(
        "generate-document/create/",
        views.F680CreateDocument.as_view(),
        name="generate_document_create",
    ),
    path(
        "generate-document/view/",
        views.F680DocumentsView.as_view(),
        name="generate_document_view",
    ),
]
