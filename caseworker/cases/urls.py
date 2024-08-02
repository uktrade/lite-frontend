from django.urls import path, include

from caseworker.cases.views import (
    main,
    advice,
    generate_document,
    ecju,
    goods,
    external_data,
    case_assignments,
    queries,
    denials,
)
from caseworker.flags.views import AssignFlags
from caseworker.cases.views.finalisation.letters import SelectInformTemplate, EditLetterText, EditInformLetterText

app_name = "cases"

urlpatterns = [
    path("", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True, "tab": "default"}),
    path("case-notes/", main.CaseNotes.as_view(), name="case_notes"),
    path("im-done/", main.ImDoneView.as_view(), name="done"),
    path("change-status/", main.ChangeStatus.as_view(), name="change_status"),
    path("change-sub-status/", main.ChangeSubStatus.as_view(), name="change_sub_status"),
    path("change-license-status/<uuid:licence_pk>/", main.ChangeLicenceStatus.as_view(), name="change_licence_status"),
    path("move/", main.MoveCase.as_view(), name="move"),
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
        "remove-assignment/",
        case_assignments.CaseAssignmentRemove.as_view(),
        name="remove-case-assignment",
    ),
    path(
        "remove-case-officer/",
        case_assignments.CaseOfficerRemove.as_view(),
        name="remove-case-officer",
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
    path("ecju-queries/<uuid:query_pk>/close-query/", queries.CloseQueryView.as_view(), name="close_query"),
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
        "generate-document/<uuid:dpk>/preview-view/<str:decision_key>",
        generate_document.PreviewViewDocument.as_view(),
        name="generate_document_preview_view",
    ),
    path(
        "generate-document/<uuid:tpk>/create/",
        generate_document.CreateDocument.as_view(),
        name="generate_document_create",
    ),
    path(
        "generate-document/<uuid:document_pk>/send/",
        generate_document.SendExistingDocument.as_view(),
        name="generate_document_send",
    ),
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
    path("denials/", denials.Denials.as_view(), name="denials"),
    path("activities/", include("caseworker.activities.urls")),
    # tabs
    path("<str:tab>/", main.CaseDetail.as_view(), name="case", kwargs={"disable_queue_lookup": True}),
    # Finalisation actions
    path(
        "letters/select-inform-template/",
        SelectInformTemplate.as_view(),
        name="select-inform-template",
    ),
    path(
        "letters/select-edit-text/<uuid:paragraph_id>/",
        EditInformLetterText.as_view(),
        name="select-edit-text",
    ),
    path(
        "<uuid:dpk>/edit-letter/<str:decision_key>",
        EditLetterText.as_view(),
        name="edit-letter-text",
    ),
]
