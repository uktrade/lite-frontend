from django.urls import include, path

from exporter.applications.views import (
    goods,
    documents,
    locations,
    additional_documents,
    common,
    edit,
    told_by_an_official,
    optional_note,
    goods_types,
    f680_details,
    clearance,
    questions,
    end_use_details,
    route_of_goods,
    export_details,
)
from exporter.applications.views.security_approvals.views import (
    SecurityApprovals,
    SecurityApprovalsSummaryView,
)

from exporter.applications.views.security_approvals.edit_views import (
    EditF680ReferenceNumber,
    EditSecurityOtherDetails,
    EditF1686Details,
    EditSecurityApprovalDetails,
)


from exporter.applications.views.goods import AddGoodsSummary, GoodsDetailSummaryCheckYourAnswers
from exporter.applications.views.parties import consignees, end_users, third_parties, ultimate_end_users
from exporter.goods.views import (
    EditGood,
    EditGrading,
    GoodComponentView,
    GoodInformationSecurityView,
    GoodMilitaryUseView,
    GoodSoftwareTechnologyView,
    EditFirearmProductTypeView,
    EditCalibreView,
    EditFirearmActDetailsView,
    EditNumberOfItemsView,
    EditIdentificationMarkingsView,
    EditSerialNumbersView,
    EditFirearmReplicaView,
    EditFirearmActCertificateDetails,
    EditYearOfManufactureView,
    UpdateSerialNumbersView,
)
from exporter.applications.views.hcsat import HCSATApplicationPage


app_name = "applications"
urlpatterns = [
    # Common
    path("", common.ApplicationsList.as_view(), name="applications"),
    path("add-serial-numbers/", goods.AddSerialNumbersList.as_view(), name="add_serial_numbers"),
    path("<uuid:pk>/delete/", common.DeleteApplication.as_view(), name="delete"),
    path("<uuid:pk>/task-list/", common.ApplicationTaskList.as_view(), name="task_list"),
    path("<uuid:pk>/summary/", common.ApplicationSummary.as_view(), name="summary"),
    path("<uuid:pk>/submit-success/", common.ApplicationSubmitSuccessPage.as_view(), name="success_page"),
    path("<uuid:pk>/hcsat/<uuid:sid>/", HCSATApplicationPage.as_view(), name="application-hcsat"),
    path("<uuid:pk>/edit-type/", common.ApplicationEditType.as_view(), name="edit_type"),
    path("<uuid:pk>/check-your-answers/", common.CheckYourAnswers.as_view(), name="check_your_answers"),
    path("<uuid:pk>/submit/", common.Submit.as_view(), name="submit"),
    path("<uuid:pk>/copy/", common.ApplicationCopy.as_view(), name="copy"),
    # Standard and Open Licence
    path("<uuid:pk>/edit/reference-name/", edit.EditReferenceName.as_view(), name="edit_reference_name"),
    path(
        "<uuid:pk>/edit/told-by-an-official/",
        told_by_an_official.ApplicationEditToldByAnOfficial.as_view(),
        name="edit_told_by_an_official",
    ),
    # HMRC Query
    path("<uuid:pk>/optional-note/", optional_note.ApplicationOptionalNote.as_view(), name="optional_note"),
    # Goods
    path("<uuid:pk>/goods/", goods.ApplicationGoodsList.as_view(), name="goods"),
    path("<uuid:pk>/goods/add-new/", goods.AddGood.as_view(), name="new_good"),
    path("<uuid:pk>/goods/component-accessory/", include("exporter.applications.views.goods.component.urls")),
    path("<uuid:pk>/goods/firearm/", include("exporter.applications.views.goods.firearm.urls")),
    path("<uuid:pk>/goods/material/", include("exporter.applications.views.goods.material.urls")),
    path("<uuid:pk>/goods/complete-item/", include("exporter.applications.views.goods.platform.urls")),
    path("<uuid:pk>/goods/technology/", include("exporter.applications.views.goods.software.urls")),
    path(
        "<uuid:pk>/goods/add-firearms-certificate/",
        goods.AttachFirearmActSectionDocument.as_view(),
        name="attach-firearms-certificate",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-firearms-certificate/",
        goods.AttachFirearmActSectionDocument.as_view(),
        name="attach-firearms-certificate-existing-good",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-software-technology/",
        GoodSoftwareTechnologyView.as_view(),
        name="good_software_technology",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/edit-military-use/", GoodMilitaryUseView.as_view(), name="good_military_use"),
    path("<uuid:pk>/goods/<uuid:good_pk>/edit-good-component/", GoodComponentView.as_view(), name="good_component"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-information-security/",
        GoodInformationSecurityView.as_view(),
        name="good_information_security",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/type/",
        EditFirearmProductTypeView.as_view(),
        name="firearm_type",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/calibre/", EditCalibreView.as_view(), name="calibre"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/year-of-manufacture/",
        EditYearOfManufactureView.as_view(),
        name="year-of-manufacture",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/replica/",
        EditFirearmReplicaView.as_view(),
        name="replica",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/firearms-act/",
        EditFirearmActDetailsView.as_view(),
        name="firearms_act",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/firearms-act-certificate/",
        EditFirearmActCertificateDetails.as_view(),
        name="firearms_act_certificate",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/identification-markings/",
        EditIdentificationMarkingsView.as_view(),
        name="identification_markings",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/number-of-items/",
        EditNumberOfItemsView.as_view(),
        name="number_of_items",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/edit-firearm-details/serial-numbers/",
        EditSerialNumbersView.as_view(),
        name="serial_numbers",
    ),
    path(
        "<uuid:pk>/goods/add-new/<uuid:good_pk>/good-detail-summary/",
        AddGoodsSummary.as_view(),
        name="add_good_summary",
    ),
    path("<uuid:pk>/goods/add-new/<uuid:good_pk>/edit-good/", EditGood.as_view(), name="edit_good"),
    path("<uuid:pk>/goods/add-new/<uuid:good_pk>/edit-grading/", EditGrading.as_view(), name="edit_grading"),
    path(
        "<uuid:pk>/goods/add-new/<uuid:good_pk>/check-document-availability/",
        goods.CheckDocumentAvailability.as_view(),
        name="check_document_availability",
    ),
    path(
        "<uuid:pk>/goods/add-new/<uuid:good_pk>/document-grading/",
        goods.CheckDocumentGrading.as_view(),
        name="document_grading",
    ),
    path("<uuid:pk>/goods/add-new/<uuid:good_pk>/attach/", goods.AttachDocument.as_view(), name="attach_documents"),
    path("<uuid:pk>/goods/add-preexisting/", goods.ExistingGoodsList.as_view(), name="preexisting_good"),
    path("<uuid:pk>/goods/<uuid:good_pk>/add/", goods.AddGoodToApplication.as_view(), name="add_good_to_application"),
    path(
        "<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/remove/",
        goods.RemovePreexistingGood.as_view(),
        name="remove_preexisting_good",
    ),
    path(
        "<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/update-serial-numbers/",
        UpdateSerialNumbersView.as_view(),
        name="update_serial_numbers",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/documents/<uuid:doc_pk>/",
        goods.GoodOnApplicationDocumentView.as_view(),
        name="good-on-application-document",
    ),
    # Platform product and non-firearm
    path("<uuid:pk>/goods/is-firearm/", goods.IsGoodFirearm.as_view(), name="is_good_firearm"),
    path("<uuid:pk>/goods/non-firearm-category/", goods.NonFirearmCategory.as_view(), name="non_firearm_category"),
    path(
        "<uuid:pk>/goods/is-material-substance/",
        goods.IsMaterialSubstanceCategory.as_view(),
        name="is_material_substance",
    ),
    # F680 details
    path("<uuid:pk>/f680-details/", f680_details.F680Details.as_view(), name="f680_details"),
    path("<uuid:pk>/questions/", questions.AdditionalInformationFormView.as_view(), name="questions"),
    # Goods Types
    path("<uuid:pk>/goods-types/", goods_types.GoodsTypeList.as_view(), name="goods_types"),
    path("<uuid:pk>/goods-types/countries/", goods_types.GoodsTypeCountries.as_view(), name="goods_countries"),
    path("<uuid:pk>/goods-types/add/", goods_types.GoodsTypeAdd.as_view(), name="add_goods_type"),
    path(
        "<uuid:pk>/goods-types/remove/<uuid:goods_type_pk>/",
        goods_types.GoodsTypeRemove.as_view(),
        name="remove_goods_type",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="goods_type_attach_document",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="goods_type_download_document",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="goods_type_delete_document",
    ),
    # Goods locations
    path("<uuid:pk>/goods-locations/", locations.GoodsLocationView.as_view(), name="location"),
    path("<uuid:pk>/goods-locations/edit/", locations.GoodsStartingPointFormView.as_view(), name="edit_location"),
    path("<uuid:pk>/goods-recipients/", locations.GoodsRecipientsFormView.as_view(), name="goods_recipients"),
    path("<uuid:pk>/goods-locations-summary/", locations.LocationsSummaryView.as_view(), name="locations_summary"),
    path("<uuid:pk>/goods-locations/existing-sites/", locations.ExistingSites.as_view(), name="existing_sites"),
    path(
        "<uuid:pk>/goods-locations/external-locations/select/",
        locations.SelectAddExternalLocation.as_view(),
        name="select_add_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/add/",
        locations.AddExternalLocation.as_view(),
        name="add_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/<uuid:ext_loc_pk>/",
        locations.RemoveExternalLocation.as_view(),
        name="remove_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/preexisting/",
        locations.AddExistingExternalLocation.as_view(),
        name="add_preexisting_external_location",
    ),
    path("<uuid:pk>/goods-locations/countries/", locations.Countries.as_view(), name="countries"),
    path("<uuid:pk>/goods-locations/destinations/", locations.StaticDestinations.as_view(), name="static_destinations"),
    path(
        "<uuid:pk>/goods-locations/countries/contract-types/select/",
        locations.ChooseContractType.as_view(),
        name="choose_contract_type",
    ),
    path(
        "<uuid:pk>/goods-locations/countries/contract-types/add/<str:country>/",
        locations.AddContractTypes.as_view(),
        name="add_contract_type",
    ),
    path(
        "<uuid:pk>/goods-locations/countries/contract-types/summary/",
        locations.CountriesAndContractTypesSummary.as_view(),
        name="countries_summary",
    ),
    # End User
    path("<uuid:pk>/end-user/", end_users.EndUser.as_view(), name="end_user"),
    path("<uuid:pk>/end-user/add/", end_users.AddEndUserView.as_view(), name="add_end_user"),
    path("<uuid:pk>/end-user/set/", end_users.SetEndUserView.as_view(), name="set_end_user"),
    path("<uuid:pk>/end-user/copy/", end_users.CopyEndUsers.as_view(), name="end_users_copy"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/", end_users.EndUser.as_view(), name="end_user"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/summary/", end_users.PartySummaryView.as_view(), name="end_user_summary"),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/sub-type/",
        end_users.PartySubTypeEditView.as_view(),
        name="end_user_edit_sub_type",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/name/", end_users.PartyNameEditView.as_view(), name="end_user_edit_name"
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/website/",
        end_users.PartyWebsiteEditView.as_view(),
        name="end_user_edit_website",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/address/",
        end_users.PartyAddressEditView.as_view(),
        name="end_user_edit_address",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/signatory/",
        end_users.PartySignatoryEditView.as_view(),
        name="end_user_edit_signatory",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/document_option/",
        end_users.PartyDocumentOptionEditView.as_view(),
        name="end_user_document_option",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/undertaking_document/",
        end_users.PartyUndertakingDocumentEditView.as_view(),
        name="end_user_edit_undertaking_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/edit/<document_type>/",
        end_users.PartyDocumentEditView.as_view(),
        name="end_user_edit_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/ec3_document/",
        end_users.PartyEC3DocumentView.as_view(),
        name="end_user_ec3_document",
    ),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/copy/", end_users.CopyEndUserView.as_view(), name="copy_end_user"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/remove/", end_users.RemoveEndUserView.as_view(), name="remove_end_user"),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/<document_pk>/",
        end_users.PartyDocumentDownloadView.as_view(),
        name="party_document_download",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/attach/",
        documents.AttachDocuments.as_view(),
        name="end_user_attach_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="end_user_download_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="end_user_delete_document",
    ),
    # Consignee
    path("<uuid:pk>/consignee/", consignees.Consignee.as_view(), name="consignee"),
    path("<uuid:pk>/consignee/add/", consignees.AddConsignee.as_view(), name="add_consignee"),
    path("<uuid:pk>/consignee/set/", consignees.SetConsignee.as_view(), name="set_consignee"),
    path("<uuid:pk>/consignee/copy/", consignees.CopyConsignees.as_view(), name="consignees_copy"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/", consignees.Consignee.as_view(), name="consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/edit/", consignees.EditConsignee.as_view(), name="edit_consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/copy/", consignees.CopyConsignee.as_view(), name="copy_consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/remove/", consignees.RemoveConsignee.as_view(), name="remove_consignee"),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/attach/",
        documents.AttachDocuments.as_view(),
        name="consignee_attach_document",
    ),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="consignee_download_document",
    ),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="consignee_delete_document",
    ),
    # End use details
    path("<uuid:pk>/end-use-details/", end_use_details.EndUseDetails.as_view(), name="end_use_details"),
    path("<uuid:pk>/route-of-goods/", route_of_goods.RouteOfGoods.as_view(), name="route_of_goods"),
    # Temporary or permanent
    path(
        "<uuid:pk>/temporary-or-permanent/",
        locations.TemporaryOrPermanentFormView.as_view(),
        name="temporary_or_permanent",
    ),
    # Temporary export details
    path(
        "<uuid:pk>/export-details/",
        export_details.ExportDetails.as_view(),
        name="export_details",
    ),
    # Security Approvals
    path(
        "<uuid:pk>/security-approvals/",
        SecurityApprovals.as_view(),
        name="security_approvals",
    ),
    path(
        "<uuid:pk>/security-approvals-summary/",
        SecurityApprovalsSummaryView.as_view(),
        name="security_approvals_summary",
    ),
    path(
        "<uuid:pk>/edit-security-approvals/",
        EditSecurityApprovalDetails.as_view(),
        name="edit_security_approvals_details",
    ),
    path(
        "<uuid:pk>/edit-security-approvals-f680-reference-number/",
        EditF680ReferenceNumber.as_view(),
        name="edit_security_approvals_f680_reference_number",
    ),
    path(
        "<uuid:pk>/edit-security-approvals-security-other-details/",
        EditSecurityOtherDetails.as_view(),
        name="edit_security_approvals_security_other_details",
    ),
    path(
        "<uuid:pk>/edit-security-approvals-f1686-details/",
        EditF1686Details.as_view(),
        name="edit_security_approvals_f1686_details",
    ),
    # Ultimate end users
    path("<uuid:pk>/ultimate-end-users/", ultimate_end_users.UltimateEndUsers.as_view(), name="ultimate_end_users"),
    path(
        "<uuid:pk>/ultimate-end-users/add/",
        ultimate_end_users.AddUltimateEndUser.as_view(),
        name="add_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/set/",
        ultimate_end_users.SetUltimateEndUser.as_view(),
        name="set_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/copy/",
        ultimate_end_users.CopyUltimateEndUsers.as_view(),
        name="ultimate_end_users_copy",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/copy/",
        ultimate_end_users.CopyUltimateEndUser.as_view(),
        name="copy_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/remove/",
        ultimate_end_users.RemoveUltimateEndUser.as_view(),
        name="remove_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/",
        ultimate_end_users.UltimateEndUsers.as_view(),
        name="ultimate_end_users",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="ultimate_end_user_attach_document",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="ultimate_end_user_download_document",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="ultimate_end_user_delete_document",
    ),
    # Third parties
    path("<uuid:pk>/third-parties/", third_parties.ThirdParties.as_view(), name="third_parties"),
    path("<uuid:pk>/third-parties/add/", third_parties.AddThirdParty.as_view(), name="add_third_party"),
    path("<uuid:pk>/third-parties/set/", third_parties.SetThirdParty.as_view(), name="set_third_party"),
    path("<uuid:pk>/third-parties/copy/", third_parties.CopyThirdParties.as_view(), name="third_parties_copy"),
    path("<uuid:pk>/third-parties/<uuid:obj_pk>/", third_parties.ThirdParties.as_view(), name="third_parties"),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/copy/", third_parties.CopyThirdParty.as_view(), name="copy_third_party"
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="third_party_attach_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="third_party_download_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="third_party_delete_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/remove",
        third_parties.RemoveThirdParty.as_view(),
        name="remove_third_party",
    ),
    # Supporting documentation
    path(
        "<uuid:pk>/additional-documents/",
        additional_documents.AdditionalDocuments.as_view(),
        name="additional_documents",
    ),
    path(
        "<uuid:pk>/additional-document/attach", documents.AttachDocuments.as_view(), name="attach_additional_document"
    ),
    path(
        "<uuid:pk>/additional-document/<uuid:obj_pk>/download",
        documents.DownloadDocument.as_view(),
        name="download_additional_document",
    ),
    path(
        "<uuid:pk>/additional-document/<uuid:obj_pk>/delete",
        documents.DeleteDocument.as_view(),
        name="delete_additional_document",
    ),
    path("<uuid:pk>/notes/", common.Notes.as_view(), name="notes"),
    path("<uuid:pk>/withdraw/", common.WithdrawApplication.as_view(), name="withdraw"),
    path("<uuid:pk>/surrender/", common.SurrenderApplication.as_view(), name="surrender"),
    path("<uuid:case_pk>/appeal/", common.AppealApplication.as_view(), name="appeal"),
    path(
        "<uuid:case_pk>/appeal/<uuid:appeal_pk>/confirmation/",
        common.AppealApplicationConfirmation.as_view(),
        name="appeal_confirmation",
    ),
    path(
        "<uuid:case_pk>/appeal/<uuid:appeal_pk>/document/<uuid:document_pk>/download/",
        documents.DownloadAppealDocument.as_view(),
        name="appeal_document",
    ),
    # Download generated documents
    path(
        "<uuid:case_pk>/documents/<uuid:document_pk>/download/",
        documents.DownloadGeneratedDocument.as_view(),
        name="download_generated_document",
    ),
    path("<uuid:pk>/clearance/", clearance.SetClearanceLevel.as_view(), name="clearance_level"),
    path("<uuid:pk>/good-detail-summary/", GoodsDetailSummaryCheckYourAnswers.as_view(), name="good_detail_summary"),
    # This HAS to be at the bottom, otherwise it will swallow other url calls
    path("<uuid:pk>/", common.ApplicationDetail.as_view(), name="application"),
    path("<uuid:pk>/exhibition-details/", common.ExhibitionDetail.as_view(), name="exhibition_details"),
    path("<uuid:pk>/declaration/", common.ApplicationDeclaration.as_view(), name="declaration"),
    path("<uuid:pk>/<str:type>/", common.ApplicationDetail.as_view(), name="application"),
]
