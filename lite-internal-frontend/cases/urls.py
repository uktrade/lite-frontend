from django.urls import path

from cases.views import main, advice, generate_document, ecju, goods_query, goods
from flags.views import AssignFlags

app_name = "cases"

urlpatterns = [
    path("", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True, "tab": "details"}),
    path("case-notes/", main.CaseNotes.as_view(), name="case_notes"),
    path("done/", main.CaseImDoneView.as_view(), name="done"),
    path("change-status/", main.ChangeStatus.as_view(), name="manage"),
    path("move/", main.MoveCase.as_view(), name="move"),
    path("additional-contacts/add/", main.AddAnAdditionalContact.as_view(), name="add_additional_contact"),
    path("attach/", main.AttachDocuments.as_view(), name="attach_documents"),
    path("documents/<str:file_pk>/", main.Document.as_view(), name="document"),
    path("assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path("coalesce-user-advice/", advice.CoalesceUserAdvice.as_view(), name="coalesce_user_advice"),
    path("coalesce-team-advice/", advice.CoalesceTeamAdvice.as_view(), name="coalesce_team_advice"),
    path("team-advice-view/", advice.ClearTeamAdvice.as_view(), name="team_advice_view"),
    path("final-advice-view/", advice.ClearFinalAdvice.as_view(), name="final_advice_view"),
    path("finalise-goods-countries/", advice.FinaliseGoodsCountries.as_view(), name="finalise_goods_countries"),
    path("finalise/", advice.Finalise.as_view(), name="finalise"),
    path("finalise/generate-documents/", advice.FinaliseGenerateDocuments.as_view(), name="finalise_documents"),
    path(
        "finalise/<str:decision_key>/generate-document/select-template/",
        generate_document.SelectTemplateFinalAdvice.as_view(),
        name="finalise_document_template",
    ),
    path(
        "finalise/<str:decision_key>/generate-document/<uuid:tpk>/edit/",
        generate_document.EditTextFinalAdvice.as_view(),
        name="finalise_document_edit_text",
    ),
    path(
        "finalise/<str:decision_key>/generate-document/<uuid:tpk>/preview/",
        generate_document.PreviewDocument.as_view(),
        name="finalise_document_preview",
    ),
    path(
        "finalise/<str:decision_key>/generate-document/<uuid:tpk>/create/",
        generate_document.CreateDocumentFinalAdvice.as_view(),
        name="finalise_document_create",
    ),
    path("ecju-queries/new/", ecju.NewECJUQueryView.as_view(), name="new_ecju_query"),
    path("respond-to-clc-query/", goods_query.RespondCLCQuery.as_view(), name="respond_to_clc_query"),
    path(
        "respond-to-pv-grading-query/", goods_query.RespondPVGradingQuery.as_view(), name="respond_to_pv_grading_query",
    ),
    path("review-goods/", goods.ReviewGoods.as_view(), name="review_goods"),
    path("generate-document/", generate_document.SelectTemplate.as_view(), name="generate_document"),
    path(
        "generate-document/<uuid:tpk>/edit/",
        generate_document.EditDocumentText.as_view(),
        name="generate_document_edit",
    ),
    path(
        "generate-document/<uuid:dpk>/",
        generate_document.RegenerateExistingDocument.as_view(),
        name="generate_document_regenerate",
    ),
    path(
        "generate-document/<uuid:tpk>/preview/",
        generate_document.PreviewDocument.as_view(),
        name="generate_document_preview",
    ),
    path(
        "generate-document/<uuid:tpk>/create/",
        generate_document.CreateDocument.as_view(),
        name="generate_document_create",
    ),
    path("case-officer/", main.CaseOfficer.as_view(), name="case_officer"),
    path("assign-user/", main.UserWorkQueue.as_view(), name="assign_user"),
    path("assign-user-queue/<uuid:user_pk>/", main.UserTeamQueue.as_view(), name="assign_user_queue"),
    path("rerun-routing-rules/", main.RerunRoutingRules.as_view(), name="rerun_routing_rules",),
    path("<str:tab>/", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True}),
    path("<str:tab>/give-advice/", advice.GiveAdvice.as_view(), name="give_advice"),
]
