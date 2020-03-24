from django.urls import path

from cases.views import main, advice, goods, goods_query, ecju, generate_document, destinations
from flags.views import AssignFlags

app_name = "cases"
urlpatterns = [
    path("", main.Cases.as_view(), name="cases"),
    path("<uuid:pk>/", main.ViewCase.as_view(), name="case"),
    path("<uuid:pk>/done/", main.CaseProcessedByUser.as_view(), name="done"),
    path("<uuid:pk>/done/<uuid:queue_id>", main.CaseProcessedByUserForQueue.as_view(), name="done_for_queue"),
    path("<uuid:pk>/change-status/", main.ChangeStatus.as_view(), name="manage"),
    path("<uuid:pk>/move/", main.MoveCase.as_view(), name="move"),
    path("<uuid:pk>/additional-contacts/", main.AdditionalContacts.as_view(), name="additional_contacts"),
    path("<uuid:pk>/additional-contacts/add/", main.AddAnAdditionalContact.as_view(), name="add_additional_contact"),
    path("<uuid:pk>/documents/", main.Documents.as_view(), name="documents"),
    path("<uuid:pk>/attach/", main.AttachDocuments.as_view(), name="attach_documents"),
    path("<uuid:pk>/documents/<str:file_pk>/", main.Document.as_view(), name="document"),
    path("<uuid:pk>/assign-flags/", AssignFlags.as_view(), name="assign_flags"),
    path("<uuid:pk>/user-advice-view/", advice.ViewUserAdvice.as_view(), name="user_advice_view"),
    path("<uuid:pk>/team-advice-view/coalesce/", advice.CoalesceUserAdvice.as_view(), name="coalesce_user_advice"),
    path("<uuid:pk>/team-advice-view/", advice.ViewTeamAdvice.as_view(), name="team_advice_view"),
    path("<uuid:pk>/final-advice-view/coalesce/", advice.CoalesceTeamAdvice.as_view(), name="coalesce_team_advice"),
    path("<uuid:pk>/final-advice-view/", advice.ViewFinalAdvice.as_view(), name="final_advice_view"),
    path("<uuid:pk>/advice-view/give-user-advice/", advice.GiveUserAdvice.as_view(), name="give_user_advice"),
    path(
        "<uuid:pk>/advice-view/give-user-advice/<str:type>/",
        advice.GiveUserAdviceDetail.as_view(),
        name="give_user_advice_detail",
    ),
    path("<uuid:pk>/advice-view/give-team-advice/", advice.GiveTeamAdvice.as_view(), name="give_team_advice"),
    path(
        "<uuid:pk>/advice-view/give-team-advice/<str:type>/",
        advice.GiveTeamAdviceDetail.as_view(),
        name="give_team_advice_detail",
    ),
    path("<uuid:pk>/advice-view/give-final-advice/", advice.GiveFinalAdvice.as_view(), name="give_final_advice"),
    path(
        "<uuid:pk>/advice-view/give-final-advice/<str:type>/",
        advice.GiveFinalAdviceDetail.as_view(),
        name="give_final_advice_detail",
    ),
    path(
        "<uuid:pk>/finalise-goods-countries/", advice.FinaliseGoodsCountries.as_view(), name="finalise_goods_countries"
    ),
    path("<uuid:pk>/finalise/", advice.Finalise.as_view(), name="finalise"),
    path(
        "<uuid:pk>/finalise/generate-documents/", advice.FinaliseGenerateDocuments.as_view(), name="finalise_documents"
    ),
    path(
        "<uuid:pk>/finalise/<str:decision_key>/generate-document/select-template/",
        generate_document.SelectTemplateFinalAdvice.as_view(),
        name="finalise_document_template",
    ),
    path(
        "<uuid:pk>/finalise/<str:decision_key>/generate-document/<uuid:tpk>/edit/",
        generate_document.EditTextFinalAdvice.as_view(),
        name="finalise_document_edit_text",
    ),
    path(
        "<uuid:pk>/finalise/<str:decision_key>/generate-document/<uuid:tpk>/add-paragraphs/",
        generate_document.AddDocumentParagraphsFinalAdvice.as_view(),
        name="finalise_document_add_paragraphs",
    ),
    path(
        "<uuid:pk>/finalise/<str:decision_key>/generate-document/<uuid:tpk>/preview/",
        generate_document.PreviewDocument.as_view(),
        name="finalise_document_preview",
    ),
    path(
        "<uuid:pk>/finalise/<str:decision_key>/generate-document/<uuid:tpk>/create/",
        generate_document.CreateDocumentFinalAdvice.as_view(),
        name="finalise_document_create",
    ),
    path("<uuid:pk>/ecju-queries/", ecju.ViewEcjuQueries.as_view(), name="ecju_queries"),
    path("<uuid:pk>/ecju-queries/add", ecju.CreateEcjuQuery.as_view(), name="ecju_queries_add"),
    path("<uuid:pk>/respond-to-clc-query/", goods_query.RespondCLCQuery.as_view(), name="respond_to_clc_query"),
    path(
        "<uuid:pk>/respond-to-clc-query/flags/",
        goods_query.RespondCLCFlags.as_view(),
        name="respond_to_clc_query_flags",
    ),
    path(
        "<uuid:pk>/respond-to-pv-grading-query/",
        goods_query.RespondPVGradingQuery.as_view(),
        name="respond_to_pv_grading_query",
    ),
    path(
        "<uuid:pk>/respond-to-pv-grading-query/flags/",
        goods_query.RespondPVGradingFlags.as_view(),
        name="respond_to_pv_grading_query_flags",
    ),
    path("<uuid:pk>/review-goods/", goods.ReviewGoods.as_view(), name="review_goods"),
    path("<uuid:pk>/review-goods-clc/", goods.ReviewGoodsClc.as_view(), name="review_goods_clc"),
    path("<uuid:pk>/generate-document/", generate_document.SelectTemplate.as_view(), name="generate_document"),
    path(
        "<uuid:pk>/generate-document/<uuid:tpk>/edit/",
        generate_document.EditDocumentText.as_view(),
        name="generate_document_edit",
    ),
    path(
        "<uuid:pk>/generate-document/<uuid:dpk>/",
        generate_document.RegenerateExistingDocument.as_view(),
        name="generate_document_regenerate",
    ),
    path(
        "<uuid:pk>/generate-document/<uuid:tpk>/add-paragraphs/",
        generate_document.AddDocumentParagraphs.as_view(),
        name="generate_document_add_paragraphs",
    ),
    path(
        "<uuid:pk>/generate-document/<uuid:tpk>/preview/",
        generate_document.PreviewDocument.as_view(),
        name="generate_document_preview",
    ),
    path(
        "<uuid:pk>/generate-document/<uuid:tpk>/create/",
        generate_document.CreateDocument.as_view(),
        name="generate_document_create",
    ),
    path(
        "<uuid:pk>/assign-destination-flags/",
        destinations.AssignDestinationFlags.as_view(),
        name="assign_destination_flags",
    ),
    path("<uuid:pk>/case-officer/", main.CaseOfficer.as_view(), name="case_officer"),
    path("<uuid:pk>/assign-user/", main.UserWorkQueue.as_view(), name="assign_user"),
    path("<uuid:pk>/assign-user-queue/<uuid:user_pk>/", main.UserTeamQueue.as_view(), name="assign_user_queue"),
]
