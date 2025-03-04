from django.urls import path

from caseworker.advice.views import consolidate, views
from caseworker.advice.views.approval import GiveApprovalAdviceView, SelectAdviceView
from caseworker.advice.views.edit import EditAdviceView

urlpatterns = [
    path("", views.AdviceView.as_view(), name="advice_view"),
    path("case-details/", views.CaseDetailView.as_view(), name="case_details"),
    path("select-advice/", SelectAdviceView.as_view(), name="select_advice"),
    path("approve-all-legacy/", views.GiveApprovalAdviceViewLegacy.as_view(), name="approve_all_legacy"),
    path("approve-all/", GiveApprovalAdviceView.as_view(), name="approve_all"),
    path("refuse-all/", views.RefusalAdviceView.as_view(), name="refuse_all"),
    path("view-my-advice/", views.AdviceDetailView.as_view(), name="view_my_advice"),
    path("edit-advice-legacy/", views.EditAdviceViewLegacy.as_view(), name="edit_advice_legacy"),
    path("edit-advice/", EditAdviceView.as_view(), name="edit_advice"),
    path("delete-advice/", views.DeleteAdviceView.as_view(), name="delete_advice"),
    path("countersign/", views.CountersignAdviceView.as_view(), name="countersign_advice_view"),
    path("countersign/review-advice/", views.ReviewCountersignView.as_view(), name="countersign_review"),
    path("countersign/view-advice/", views.ViewCountersignedAdvice.as_view(), name="countersign_view"),
    path("countersign/edit-advice/", views.CountersignEditAdviceView.as_view(), name="countersign_edit"),
    path(
        "countersign/decision/review-advice/",
        views.ReviewCountersignDecisionAdviceView.as_view(),
        name="countersign_decision_review",
    ),
    path(
        "countersign/decision/edit-advice/",
        views.EditCountersignDecisionAdviceView.as_view(),
        name="countersign_decision_edit",
    ),
    path("consolidate/", views.ConsolidateAdviceView.as_view(), name="consolidate_advice_view"),
    path("consolidate/review/", consolidate.ConsolidateSelectDecisionView.as_view(), name="consolidate_review"),
    path("consolidate/review/approve/", consolidate.ConsolidateApproveView.as_view(), name="consolidate_approve"),
    path("consolidate/review/refuse/", consolidate.ConsolidateRefuseView.as_view(), name="consolidate_refuse"),
    path(
        "consolidate/review/lu-refuse/",
        consolidate.LUConsolidateRefuseView.as_view(),
        name="consolidate_refuse_lu",
    ),
    path("consolidate/edit/", views.ConsolidateEditView.as_view(), name="consolidate_edit"),
    path("consolidate/view-advice/", views.ViewConsolidatedAdviceView.as_view(), name="consolidate_view"),
    path("assess-trigger-list-products/", views.DESNZProductAssessmentView.as_view(), name="assess_trigger_list"),
    path(
        "edit-trigger-list-products/<uuid:good_on_application_id>/",
        views.DESNZProductAssessmentEditView.as_view(),
        name="edit_trigger_list",
    ),
    path(
        "clear-trigger-list-assessments/",
        views.DESNZProductClearAssessmentsView.as_view(),
        name="clear_trigger_list_assessments",
    ),
]
