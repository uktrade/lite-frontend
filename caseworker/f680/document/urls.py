from django.urls import path

from caseworker.f680.document import views


app_name = "document"

urlpatterns = [
    path(
        "",
        views.DocumentGenerationView.as_view(),
        name="all",
    ),
    path(
        "<uuid:template_id>/generate/",
        views.F680GenerateDocument.as_view(),
        name="generate",
    ),
]
