from django.urls import path

from caseworker.f680.document import views


app_name = "document"

urlpatterns = [
    path(
        "generation/",
        views.DocumentGenerationView.as_view(),
        name="generation",
    ),
]
