from django.urls import path

from caseworker.advice import views

urlpatterns = [
    path("", views.AdviceView.as_view(), name="advice_view"),
    path("case-details/", views.CaseDetailView.as_view(), name="case_details"),
    path("select-advice/", views.SelectAdviceView.as_view(), name="select_advice"),
    path("approve-all/", views.GiveApprovalAdviceView.as_view(), name="approve_all"),
    path("refuse-all/", views.RefusalAdviceView.as_view(), name="refuse_all"),
    path("view-my-advice/", views.AdviceDetailView.as_view(), name="view_my_advice"),
    path("edit-advice/", views.EditAdviceView.as_view(), name="edit_advice"),
    path("delete-advice/", views.DeleteAdviceView.as_view(), name="delete_advice"),
    path("countersign/", views.CountersignAdviceView.as_view(), name="countersign_advice_view"),
    path("countersign/review-advice/", views.ReviewCountersignView.as_view(), name="countersign_review"),
    path("countersign/view-advice/", views.ViewCountersignedAdvice.as_view(), name="countersign_view"),
    path("countersign/edit-advice/", views.CountersignEditAdviceView.as_view(), name="countersign_edit"),
    path("consolidate/", views.ConsolidateAdviceView.as_view(), name="consolidate_advice_view"),
    path("consolidate/review/<advice_type>/", views.ReviewConsolidateView.as_view()),
    path("consolidate/review/", views.ReviewConsolidateView.as_view(), name="consolidate_review"),
    path("consolidate/edit/", views.ConsolidateEditView.as_view(), name="consolidate_edit"),
    path("consolidate/view-advice/", views.ViewConsolidatedAdviceView.as_view(), name="consolidate_view"),
]
