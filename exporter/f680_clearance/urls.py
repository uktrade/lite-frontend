from django.urls import include, path

from . import views


app_name = "f680_clearance"

urlpatterns = [
    path("apply/", views.F680ApplicationCreateView.as_view(), name="apply"),
    path("<uuid:pk>/apply/", views.F680ApplicationSummaryView.as_view(), name="task_list"),
    path(
        "<uuid:pk>/general-application-details/",
        include("exporter.f680_clearance.application_sections.general_application_details.urls"),
    ),
    path(
        "<uuid:pk>/approval-details/",
        include("exporter.f680_clearance.application_sections.approval_details.urls"),
    ),
    path(
        "<uuid:pk>/additional-information/",
        include("exporter.f680_clearance.application_sections.additional_information.urls"),
    ),
    path(
        "<uuid:pk>/user-information/",
        include("exporter.f680_clearance.application_sections.user_information.urls"),
    ),
]
