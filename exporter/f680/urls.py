from django.urls import include, path

from . import views


app_name = "f680"

urlpatterns = [
    path("<uuid:pk>/apply/", views.F680ApplicationSummaryView.as_view(), name="summary"),
    path("<uuid:pk>/declaration/", views.F680DeclarationView.as_view(), name="declaration"),
    path("<uuid:pk>/summary/", views.F680SubmittedApplicationSummaryView.as_view(), name="submitted_summary"),
    path(
        "<uuid:pk>/summary/<str:type>/", views.F680SubmittedApplicationSummaryView.as_view(), name="submitted_summary"
    ),
    path(
        "<uuid:pk>/general-application-details/",
        include("exporter.f680.application_sections.general_application_details.urls"),
    ),
    path(
        "<uuid:pk>/approval-details/",
        include("exporter.f680.application_sections.approval_details.urls"),
    ),
    path(
        "<uuid:pk>/additional-information/",
        include("exporter.f680.application_sections.additional_information.urls"),
    ),
    path(
        "<uuid:pk>/user-information/",
        include("exporter.f680.application_sections.user_information.urls"),
    ),
    path(
        "<uuid:pk>/supporting-documents/",
        include("exporter.f680.application_sections.supporting_documents.urls"),
    ),
]
