from django.urls import path

from caseworker.advice import views

urlpatterns = [
    path("", views.AdvicePlaceholderView.as_view(), name="advice_placeholder"),
    path("case-details/", views.CaseDetailView.as_view(), name="case_details"),
    path("approve-all/", views.GiveApprovalAdviceView.as_view(), name="approve_all"),
]
