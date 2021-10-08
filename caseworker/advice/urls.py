from django.urls import path

from caseworker.advice.views import CaseDetailView, AdvicePlaceholderView

urlpatterns = [
    path("", AdvicePlaceholderView.as_view(), name="advice_placeholder"),
    path("case-details/", CaseDetailView.as_view(), name="case_details"),
]
