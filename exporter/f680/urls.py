from django.urls import include, path

from . import views


app_name = "f680"

urlpatterns = [
    path("apply/", views.F680ApplicationCreateView.as_view(), name="apply"),
    path("<uuid:pk>/apply/", views.F680ApplicationSummaryView.as_view(), name="summary"),
    path(
        "<uuid:pk>/general-application-details/",
        include("exporter.f680.application_sections.general_application_details.urls"),
    ),
]
