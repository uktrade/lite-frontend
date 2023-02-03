from django.urls import path

from caseworker.report_summary import views

app_name = "report_summary"

urlpatterns = [
    path("prefix", views.ReportSummaryPrefix.as_view(), name="prefix"),
    path("subject", views.ReportSummarySubject.as_view(), name="subject"),
]
