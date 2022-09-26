from django.urls import path

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
from exporter.applications.views.goods.add_good_firearm.views.add import AddGoodFirearm, AddGoodFirearmToApplication
from exporter.applications.views.goods.add_good_firearm.views.attach import AttachFirearmToApplication
from exporter.applications.views.goods.add_good_firearm.views.edit import (
    FirearmEditCalibre,
    FirearmEditCategory,
    FirearmEditControlListEntry,
    FirearmEditFirearmsAct1968,
    FirearmEditLetterOfAuthority,
    FirearmEditSection5FirearmsAct1968,
    FirearmEditName,
    FirearmEditReplica,
    FirearmEditProductDescriptionView,
    FirearmEditProductDocumentView,
    FirearmEditProductDocumentSensitivity,
    FirearmEditProductDocumentAvailability,
    FirearmEditPVGrading,
    FirearmEditPVGradingDetails,
    FirearmEditRegisteredFirearmsDealer,
    FirearmProductOnApplicationSummaryEditFirearmCertificate,
    FirearmProductOnApplicationSummaryEditIsDeactivated,
    FirearmProductOnApplicationSummaryEditIsDeactivatedToStandard,
    FirearmProductOnApplicationSummaryEditMadeBefore1938,
    FirearmProductOnApplicationSummaryEditOnwardAltered,
    FirearmProductOnApplicationSummaryEditOnwardExported,
    FirearmProductOnApplicationSummaryEditOnwardIncorporated,
    FirearmProductOnApplicationSummaryEditQuantityValue,
    FirearmProductOnApplicationSummaryEditSerialIdentificationMarkings,
    FirearmProductOnApplicationSummaryEditSerialNumbers,
    FirearmProductOnApplicationSummaryEditShotgunCertificate,
    FirearmProductOnApplicationSummaryEditYearOfManufacture,
)
from exporter.applications.views.goods.add_good_firearm.views.summary import (
    FirearmAttachProductOnApplicationSummary,
    FirearmProductSummary,
    FirearmProductOnApplicationSummary,
)

from exporter.applications.views.goods.add_good_platform.views.add import AddGoodPlatform, AddGoodPlatformToApplication
from exporter.applications.views.goods.add_good_platform.views.edit import (
    PlatformEditControlListEntry,
    PlatformEditMilitaryUseView,
    PlatformEditName,
    PlatformEditPartNumberView,
    PlatformEditProductDescriptionView,
    PlatformEditProductDocumentAvailability,
    PlatformEditProductDocumentSensitivity,
    PlatformEditProductDocumentView,
    PlatformEditPVGrading,
    PlatformEditPVGradingDetails,
    PlatformEditUsesInformationSecurity,
    PlatformOnApplicationSummaryEditOnwardAltered,
    PlatformOnApplicationSummaryEditOnwardExported,
    PlatformOnApplicationSummaryEditOnwardIncorporated,
    PlatformOnApplicationSummaryEditQuantityValue,
)
from exporter.applications.views.goods.add_good_platform.views.summary import (
    PlatformProductOnApplicationSummary,
    PlatformProductSummary,
)
from exporter.applications.views.goods.add_good_material.views.add import AddGoodMaterial, AddGoodMaterialToApplication
from exporter.applications.views.goods.add_good_material.views.summary import (
    MaterialProductOnApplicationSummary,
    MaterialProductSummary,
)
from exporter.applications.views.goods.add_good_material.views.edit import (
    MaterialEditControlListEntry,
    MaterialEditMilitaryUseView,
    MaterialEditName,
    MaterialEditProductDescriptionView,
    MaterialEditProductDocumentAvailability,
    MaterialEditProductDocumentSensitivity,
    MaterialEditProductDocumentView,
    MaterialEditPartNumberView,
    MaterialEditPVGrading,
    MaterialEditPVGradingDetails,
    MaterialOnApplicationSummaryEditOnwardExported,
    MaterialOnApplicationSummaryEditOnwardAltered,
    MaterialOnApplicationSummaryEditOnwardIncorporated,
    MaterialOnApplicationSummaryEditUnitQuantityValue,
)
from exporter.applications.views.goods.add_good_component.views.add import (
    AddGoodComponent,
    AddGoodComponentToApplication,
)
from exporter.applications.views.goods.add_good_component.views.summary import (
    ComponentProductOnApplicationSummary,
    ComponentProductSummary,
)
from exporter.applications.views.goods.add_good_component.views.edit import (
    ComponentEditControlListEntry,
    ComponentEditMilitaryUseView,
    ComponentEditName,
    ComponentEditComponentDetails,
    ComponentEditPartNumberView,
    ComponentEditProductDescriptionView,
    ComponentEditProductDocumentAvailability,
    ComponentEditProductDocumentSensitivity,
    ComponentEditProductDocumentView,
    ComponentEditPVGrading,
    ComponentEditPVGradingDetails,
    ComponentEditUsesInformationSecurity,
    ComponentOnApplicationSummaryEditOnwardAltered,
    ComponentOnApplicationSummaryEditOnwardExported,
    ComponentOnApplicationSummaryEditOnwardIncorporated,
    ComponentOnApplicationSummaryEditQuantityValue,
)
from exporter.applications.views.goods.add_good_software.views.add import AddGoodSoftware, AddGoodSoftwareToApplication
from exporter.applications.views.goods.add_good_software.views.edit import (
    SoftwareEditControlListEntry,
    SoftwareEditName,
    SoftwareEditPVGrading,
    SoftwareEditPVGradingDetails,
    SoftwareEditSecurityFeatures,
    SoftwareEditDeclaredAtCustoms,
    SoftwareEditProductDocumentAvailability,
    SoftwareEditProductDocumentSensitivity,
    SoftwareEditProductDocumentView,
    SoftwareEditProductDescriptionView,
    SoftwareEditPartNumberView,
    SoftwareEditMilitaryUseView,
    SoftwareOnApplicationSummaryEditOnwardExported,
    SoftwareOnApplicationSummaryEditOnwardAltered,
    SoftwareOnApplicationSummaryEditOnwardIncorporated,
    SoftwareOnApplicationSummaryEditQuantityValue,
)
from exporter.applications.views.goods.add_good_software.views.summary import (
    SoftwareProductSummary,
    SoftwareProductOnApplicationSummary,
)

app_name = "applications"
urlpatterns = [
    # Common
    path("", common.ApplicationsList.as_view(), name="applications"),
    path("add-serial-numbers/", goods.AddSerialNumbersList.as_view(), name="add_serial_numbers"),
    path("<uuid:pk>/delete/", common.DeleteApplication.as_view(), name="delete"),
    path("<uuid:pk>/task-list/", common.ApplicationTaskList.as_view(), name="task_list"),
    path("<uuid:pk>/summary/", common.ApplicationSummary.as_view(), name="summary"),
    path("<uuid:pk>/submit-success/", common.ApplicationSubmitSuccessPage.as_view(), name="success_page"),
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
    path("<uuid:pk>/goods/add-new/firearm/", AddGoodFirearm.as_view(), name="new_good_firearm"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-new/firearm-to-application/",
        AddGoodFirearmToApplication.as_view(),
        name="new_good_firearm_to_application",
    ),
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
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/category/",
        FirearmEditCategory.as_view(),
        name="firearm_edit_category",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/name/", FirearmEditName.as_view(), name="firearm_edit_name"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/control-list-entries/",
        FirearmEditControlListEntry.as_view(),
        name="firearm_edit_control_list_entries",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/calibre/",
        FirearmEditCalibre.as_view(),
        name="firearm_edit_calibre",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/replica/",
        FirearmEditReplica.as_view(),
        name="firearm_edit_replica",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/pv-grading/",
        FirearmEditPVGrading.as_view(),
        name="firearm_edit_pv_grading",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/pv-grading-details/",
        FirearmEditPVGradingDetails.as_view(),
        name="firearm_edit_pv_grading_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/product-document-availability/",
        FirearmEditProductDocumentAvailability.as_view(),
        name="firearm_edit_product_document_availability",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/product-document-sensitivity/",
        FirearmEditProductDocumentSensitivity.as_view(),
        name="firearm_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/product-document/",
        FirearmEditProductDocumentView.as_view(),
        name="firearm_edit_product_document",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/product-description/",
        FirearmEditProductDescriptionView.as_view(),
        name="firearm_edit_product_description",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/registered-firearms-dealer/",
        FirearmEditRegisteredFirearmsDealer.as_view(),
        name="firearm_edit_registered_firearms_dealer",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/section-5-firearms-act-1968/",
        FirearmEditSection5FirearmsAct1968.as_view(),
        name="firearm_edit_section_5_firearms_act_1968",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/letter-of-authority/",
        FirearmEditLetterOfAuthority.as_view(),
        name="firearm_edit_letter_of_authority",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/firearm/edit/firearms-act-1968/",
        FirearmEditFirearmsAct1968.as_view(),
        name="firearm_edit_firearms_act_1968",
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
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_pk>/product-summary/",
        FirearmProductSummary.as_view(),
        name="firearm_product_summary",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/product-on-application-summary/",
        FirearmProductOnApplicationSummary.as_view(),
        name="product_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/attach-product-on-application-summary/",
        FirearmAttachProductOnApplicationSummary.as_view(),
        name="attach_product_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/firearm-certificate/",
        FirearmProductOnApplicationSummaryEditFirearmCertificate.as_view(),
        name="product_on_application_summary_edit_firearm_certificate",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/shotgun-certificate/",
        FirearmProductOnApplicationSummaryEditShotgunCertificate.as_view(),
        name="product_on_application_summary_edit_shotgun_certificate",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/made-before-1938/",
        FirearmProductOnApplicationSummaryEditMadeBefore1938.as_view(),
        name="product_on_application_summary_edit_made_before_1938",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/year-of-manufacture/",
        FirearmProductOnApplicationSummaryEditYearOfManufacture.as_view(),
        name="product_on_application_summary_edit_year_of_manufacture",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        FirearmProductOnApplicationSummaryEditOnwardExported.as_view(),
        name="product_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        FirearmProductOnApplicationSummaryEditOnwardAltered.as_view(),
        name="product_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        FirearmProductOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="product_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/is-deactivated/",
        FirearmProductOnApplicationSummaryEditIsDeactivated.as_view(),
        name="product_on_application_summary_edit_is_deactivated",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/is-deactivated-to-standard/",
        FirearmProductOnApplicationSummaryEditIsDeactivatedToStandard.as_view(),
        name="product_on_application_summary_edit_is_deactivated_to_standard",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        FirearmProductOnApplicationSummaryEditQuantityValue.as_view(),
        name="product_on_application_summary_edit_quantity_value",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/serial-identification-markings/",
        FirearmProductOnApplicationSummaryEditSerialIdentificationMarkings.as_view(),
        name="product_on_application_summary_edit_serial_identification_markings",
    ),
    path(
        "<uuid:pk>/goods/firearm/<uuid:good_on_application_pk>/<str:summary_type>/edit/serial-numbers/",
        FirearmProductOnApplicationSummaryEditSerialNumbers.as_view(),
        name="product_on_application_summary_edit_serial_numbers",
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
        "<uuid:pk>/goods/<uuid:good_pk>/add/firearm/",
        AttachFirearmToApplication.as_view(),
        name="attach_firearm_to_application",
    ),
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
    path("<uuid:pk>/goods/add-new/platform/", AddGoodPlatform.as_view(), name="new_good_platform"),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_pk>/product-summary/",
        PlatformProductSummary.as_view(),
        name="platform_product_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-new/platform-to-application/",
        AddGoodPlatformToApplication.as_view(),
        name="new_good_platform_to_application",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/platform-on-application-summary/",
        PlatformProductOnApplicationSummary.as_view(),
        name="platform_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add/platform/",
        AddGoodPlatformToApplication.as_view(),
        name="attach_platform_to_application",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add/software/",
        AddGoodSoftwareToApplication.as_view(),
        name="attach_software_to_application",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/platform/edit/name/", PlatformEditName.as_view(), name="platform_edit_name"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/control-list-entries/",
        PlatformEditControlListEntry.as_view(),
        name="platform_edit_control_list_entries",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/pv-grading/",
        PlatformEditPVGrading.as_view(),
        name="platform_edit_pv_grading",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/pv-grading-details/",
        PlatformEditPVGradingDetails.as_view(),
        name="platform_edit_pv_grading_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/uses-information-security/",
        PlatformEditUsesInformationSecurity.as_view(),
        name="platform_edit_uses_information_security",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/product-document-availability/",
        PlatformEditProductDocumentAvailability.as_view(),
        name="platform_edit_product_document_availability",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/product-document-sensitivity/",
        PlatformEditProductDocumentSensitivity.as_view(),
        name="platform_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/product-document/",
        PlatformEditProductDocumentView.as_view(),
        name="platform_edit_product_document",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/product-description/",
        PlatformEditProductDescriptionView.as_view(),
        name="platform_edit_product_description",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/part-number/",
        PlatformEditPartNumberView.as_view(),
        name="platform_edit_part_number",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/platform/edit/military-use/",
        PlatformEditMilitaryUseView.as_view(),
        name="platform_edit_military_use",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        PlatformOnApplicationSummaryEditOnwardExported.as_view(),
        name="platform_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        PlatformOnApplicationSummaryEditOnwardAltered.as_view(),
        name="platform_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        PlatformOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="platform_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        PlatformOnApplicationSummaryEditQuantityValue.as_view(),
        name="platform_on_application_summary_edit_quantity_value",
    ),
    path("<uuid:pk>/goods/add-new/component/", AddGoodComponent.as_view(), name="new_good_component"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-new/component-to-application/",
        AddGoodComponentToApplication.as_view(),
        name="new_good_component_to_application",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add/component/",
        AddGoodComponentToApplication.as_view(),
        name="attach_component_to_application",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_pk>/product-summary/",
        ComponentProductSummary.as_view(),
        name="component_product_summary",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_on_application_pk>/component-on-application-summary/",
        ComponentProductOnApplicationSummary.as_view(),
        name="component_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/name/", ComponentEditName.as_view(), name="component_edit_name"
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/component-details/",
        ComponentEditComponentDetails.as_view(),
        name="component_edit_component_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/control-list-entries/",
        ComponentEditControlListEntry.as_view(),
        name="component_edit_control_list_entries",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/pv-grading/",
        ComponentEditPVGrading.as_view(),
        name="component_edit_pv_grading",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/pv-grading-details/",
        ComponentEditPVGradingDetails.as_view(),
        name="component_edit_pv_grading_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/uses-information-security/",
        ComponentEditUsesInformationSecurity.as_view(),
        name="component_edit_uses_information_security",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/product-document-availability/",
        ComponentEditProductDocumentAvailability.as_view(),
        name="component_edit_product_document_availability",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/product-document-sensitivity/",
        ComponentEditProductDocumentSensitivity.as_view(),
        name="component_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/product-document/",
        ComponentEditProductDocumentView.as_view(),
        name="component_edit_product_document",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/product-description/",
        ComponentEditProductDescriptionView.as_view(),
        name="component_edit_product_description",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/part-number/",
        ComponentEditPartNumberView.as_view(),
        name="component_edit_part_number",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/component/edit/military-use/",
        ComponentEditMilitaryUseView.as_view(),
        name="component_edit_military_use",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        ComponentOnApplicationSummaryEditOnwardExported.as_view(),
        name="component_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        ComponentOnApplicationSummaryEditOnwardAltered.as_view(),
        name="component_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        ComponentOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="component_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:pk>/goods/component/<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        ComponentOnApplicationSummaryEditQuantityValue.as_view(),
        name="component_on_application_summary_edit_quantity_value",
    ),
    # Material product
    path("<uuid:pk>/goods/add-new/material/", AddGoodMaterial.as_view(), name="new_good_material"),
    path(
        "<uuid:pk>/goods/material/<uuid:good_pk>/product-summary/",
        MaterialProductSummary.as_view(),
        name="material_product_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-new/material-to-application/",
        AddGoodMaterialToApplication.as_view(),
        name="new_good_material_to_application",
    ),
    path(
        "<uuid:pk>/goods/platform/<uuid:good_on_application_pk>/material-on-application-summary/",
        MaterialProductOnApplicationSummary.as_view(),
        name="material_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add/material/",
        AddGoodMaterialToApplication.as_view(),
        name="attach_material_to_application",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/material/edit/name/", MaterialEditName.as_view(), name="material_edit_name"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/control-list-entries/",
        MaterialEditControlListEntry.as_view(),
        name="material_edit_control_list_entries",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/pv-grading/",
        MaterialEditPVGrading.as_view(),
        name="material_edit_pv_grading",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/pv-grading-details/",
        MaterialEditPVGradingDetails.as_view(),
        name="material_edit_pv_grading_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/product-document-availability/",
        MaterialEditProductDocumentAvailability.as_view(),
        name="material_edit_product_document_availability",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/product-document-sensitivity/",
        MaterialEditProductDocumentSensitivity.as_view(),
        name="material_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/product-document/",
        MaterialEditProductDocumentView.as_view(),
        name="material_edit_product_document",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/product-description/",
        MaterialEditProductDescriptionView.as_view(),
        name="material_edit_product_description",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/part-number/",
        MaterialEditPartNumberView.as_view(),
        name="material_edit_part_number",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/material/edit/military-use/",
        MaterialEditMilitaryUseView.as_view(),
        name="material_edit_military_use",
    ),
    path(
        "<uuid:pk>/goods/material/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        MaterialOnApplicationSummaryEditOnwardExported.as_view(),
        name="material_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:pk>/goods/material/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        MaterialOnApplicationSummaryEditOnwardAltered.as_view(),
        name="material_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:pk>/goods/material/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        MaterialOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="material_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:pk>/goods/material/<uuid:good_on_application_pk>/<str:summary_type>/edit/unit-quantity-value/",
        MaterialOnApplicationSummaryEditUnitQuantityValue.as_view(),
        name="material_on_application_summary_edit_unit_quantity_value",
    ),
    # Software product and non-firearm
    path("<uuid:pk>/goods/add-new/software/", AddGoodSoftware.as_view(), name="new_good_software"),
    path(
        "<uuid:pk>/goods/software/<uuid:good_pk>/product-summary/",
        SoftwareProductSummary.as_view(),
        name="software_product_summary",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/add-new/software-to-application/",
        AddGoodSoftwareToApplication.as_view(),
        name="new_good_software_to_application",
    ),
    path(
        "<uuid:pk>/goods/software/<uuid:good_on_application_pk>/software-on-application-summary/",
        SoftwareProductOnApplicationSummary.as_view(),
        name="software_on_application_summary",
    ),
    path(
        "<uuid:pk>/goods/software/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        SoftwareOnApplicationSummaryEditOnwardExported.as_view(),
        name="software_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:pk>/goods/software/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        SoftwareOnApplicationSummaryEditOnwardAltered.as_view(),
        name="software_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:pk>/goods/software/<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        SoftwareOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="software_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:pk>/goods/software/<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        SoftwareOnApplicationSummaryEditQuantityValue.as_view(),
        name="software_on_application_summary_edit_quantity_value",
    ),
    path("<uuid:pk>/goods/<uuid:good_pk>/software/edit/name/", SoftwareEditName.as_view(), name="software_edit_name"),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/control-list-entries/",
        SoftwareEditControlListEntry.as_view(),
        name="software_edit_control_list_entries",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/pv-grading/",
        SoftwareEditPVGrading.as_view(),
        name="software_edit_pv_grading",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/pv-grading-details/",
        SoftwareEditPVGradingDetails.as_view(),
        name="software_edit_pv_grading_details",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/security-features/",
        SoftwareEditSecurityFeatures.as_view(),
        name="software_edit_security_features",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/declared-at-customs/",
        SoftwareEditDeclaredAtCustoms.as_view(),
        name="software_edit_declared_at_customs",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/product-document-availability/",
        SoftwareEditProductDocumentAvailability.as_view(),
        name="software_edit_product_document_availability",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/product-document-sensitivity/",
        SoftwareEditProductDocumentSensitivity.as_view(),
        name="software_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/product-document/",
        SoftwareEditProductDocumentView.as_view(),
        name="software_edit_product_document",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/product-description/",
        SoftwareEditProductDescriptionView.as_view(),
        name="software_edit_product_description",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/part-number/",
        SoftwareEditPartNumberView.as_view(),
        name="software_edit_part_number",
    ),
    path(
        "<uuid:pk>/goods/<uuid:good_pk>/software/edit/military-use/",
        SoftwareEditMilitaryUseView.as_view(),
        name="software_edit_military_use",
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
