from django.urls import path, include

from caseworker.cases.views import main, advice, generate_document, ecju, goods_query, goods, compliance, external_data
from caseworker.flags.views import AssignFlags

app_name = "cases"

urlpatterns = [
    path("", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True, "tab": "details"}),
    path("case-notes/", main.CaseNotes.as_view(), name="case_notes"),
    path("im-done/", main.ImDoneView.as_view(), name="done"),
    path("change-status/", main.ChangeStatus.as_view(), name="manage"),
    path("move/", main.MoveCase.as_view(), name="move"),
    path("additional-contacts/add/", main.AddAnAdditionalContact.as_view(), name="add_additional_contact"),
    path("attach/", main.AttachDocuments.as_view(), name="attach_documents"),
    # This needs to be before "case" path b/c the regex in that sinks everything
    path("advice/", include("caseworker.advice.urls")),
    path("tau/", include("caseworker.tau.urls")),
    path("documents/<str:file_pk>/", main.Document.as_view(), name="document"),
    path("assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path(
        "remove-matching-denials/",
        external_data.RemoveMatchingDenials.as_view(),
        name="remove-matching-denials",
    ),
    path(
        "remove-matching-sanction/",
        external_data.SanctionRevokeView.as_view(),
        name="remove-matching-sanctions",
    ),
    path(
        "matching-denials/<str:category>/",
        external_data.MatchingDenials.as_view(),
        name="matching-denials",
    ),
    path("coalesce-user-advice/", advice.CoalesceUserAdvice.as_view(), name="coalesce_user_advice"),
    path("coalesce-team-advice/", advice.CoalesceTeamAdvice.as_view(), name="coalesce_team_advice"),
    path("team-advice-view/", advice.ClearTeamAdvice.as_view(), name="team_advice_view"),
    path("final-advice-view/", advice.ClearFinalAdvice.as_view(), name="final_advice_view"),
    path("finalise-goods-countries/", advice.FinaliseGoodsCountries.as_view(), name="finalise_goods_countries"),
    path("finalise/", advice.Finalise.as_view(), name="finalise"),
    path("finalise/generate-documents/", advice.FinaliseGenerateDocuments.as_view(), name="finalise_documents"),
    path(
        "finalise/<str:decision_key>/generate-document/",
        generate_document.GenerateDecisionDocument.as_view(),
        name="finalise_document_template",
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
        "respond-to-pv-grading-query/",
        goods_query.RespondPVGradingQuery.as_view(),
        name="respond_to_pv_grading_query",
    ),
    path(
        "review-standard-application-goods/",
        goods.ReviewStandardApplicationGoodWizardView.as_view(),
        name="review_standard_application_goods",
    ),
    path(
        "review-open-application-goods/",
        goods.ReviewOpenApplicationGoodWizardView.as_view(),
        name="review_open_application_goods",
    ),
    path("generate-document/", generate_document.GenerateDocument.as_view(), name="generate_document"),
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
    path("review-date/", main.NextReviewDate.as_view(), name="review_date"),
    path("assign-user/", main.UserWorkQueue.as_view(), name="assign_user"),
    path("assign-user-queue/<uuid:user_pk>/", main.UserTeamQueue.as_view(), name="assign_user_queue"),
    path(
        "rerun-routing-rules/",
        main.RerunRoutingRules.as_view(),
        name="rerun_routing_rules",
    ),
    path(
        "reissue-ogl/",
        main.ReissueOGL.as_view(),
        name="reissue_ogl",
    ),
    path("good/<uuid:good_pk>/", goods.GoodDetails.as_view(), name="good"),
    # Compliance
    path("create-visit-report/", compliance.CreateVisitReport.as_view(), name="create_visit_report"),
    path("visit-report/", compliance.VisitReportDetails.as_view(), name="visit_report"),
    path("people-present/", compliance.PeoplePresent.as_view(), name="people_present"),
    path("overview/", compliance.Overview.as_view(), name="overview"),
    path("inspection/", compliance.Inspection.as_view(), name="inspection"),
    path("compliance-licence/", compliance.ComplianceWithLicences.as_view(), name="compliance_with_licences"),
    path("knowledge-people/", compliance.KnowledgePeople.as_view(), name="knowledge_of_people"),
    path("knowledge-products/", compliance.KnowledgeProduct.as_view(), name="knowledge_of_products"),
    path("denials/", main.Denials.as_view(), name="denials"),
    # tabs
    path("<str:tab>/", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True}),
    path("<str:tab>/give-advice/", advice.GiveAdvice.as_view(), name="give_advice"),
]
