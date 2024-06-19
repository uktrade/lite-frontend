from django.conf import settings
from django.urls import path

from exporter.goods import views
from exporter.goods.common import views as common_views
from exporter.goods.component.views import ComponentAccessoryProductDetails
from exporter.goods.firearms.views import (
    ComponentsForFirearmsAmmunitionProductDetails,
    ComponentsForFirearmsProductDetails,
    FirearmsAccessoryProductDetails,
    FirearmProductDetails,
    FirearmAmmunitionProductDetails,
    SoftwareRelatedToFirearmsProductDetails,
    TechnologyRelatedToFirearmsProductDetails,
)
from exporter.goods.materials.views import MaterialProductDetails
from exporter.goods.software.views import TechnologyProductDetails
from exporter.goods.platform.views import CompleteItemProductDetails

app_name = "goods"
urlpatterns = [
    path("", views.Goods.as_view(), name="goods"),
    path("archived-goods/", views.ArchivedGoods.as_view(), name="archived_goods"),
    path("<uuid:pk>/edit/", views.EditGood.as_view(), name="edit"),
    path("<uuid:pk>/software-technology/", views.GoodSoftwareTechnologyView.as_view(), name="good_software_technology"),
    path("<uuid:pk>/military-use/", views.GoodMilitaryUseView.as_view(), name="good_military_use"),
    path("<uuid:pk>/good-component/", views.GoodComponentView.as_view(), name="good_component"),
    path(
        "<uuid:pk>/information-security/", views.GoodInformationSecurityView.as_view(), name="good_information_security"
    ),
    path("<uuid:pk>/edit-grading/", views.EditGrading.as_view(), name="edit_grading"),
    path("<uuid:pk>/edit-firearm-details/type/", views.EditFirearmProductTypeView.as_view(), name="firearm_type"),
    path(
        "<uuid:pk>/edit-firearm-details/year-of-manufacture/",
        views.EditYearOfManufactureView.as_view(),
        name="year-of-manufacture",
    ),
    path(
        "<uuid:pk>/edit-firearm-details/replica/",
        views.EditFirearmReplicaView.as_view(),
        name="replica",
    ),
    path("<uuid:pk>/edit-firearm-details/calibre/", views.EditCalibreView.as_view(), name="calibre"),
    path(
        "<uuid:pk>/edit-firearm-details/firearms-act/", views.EditFirearmActDetailsView.as_view(), name="firearms_act"
    ),
    path(
        "<uuid:pk>/edit-firearm-details/identification_markings/",
        views.EditIdentificationMarkingsView.as_view(),
        name="identification_markings",
    ),
    path("<uuid:pk>/delete/", views.DeleteGood.as_view(), name="delete"),
    path(
        "<uuid:pk>/check-document-availability/",
        views.CheckDocumentAvailable.as_view(),
        name="check_document_availability",
    ),
    path(
        "<uuid:pk>/check-document-sensitivity/", views.CheckDocumentGrading.as_view(), name="check_document_sensitivity"
    ),
    path("<uuid:pk>/documents/<uuid:file_pk>/", views.Document.as_view(), name="document"),
    path("<uuid:pk>/documents/<uuid:file_pk>/delete/", views.DeleteDocument.as_view(), name="delete_document"),
    path("<uuid:pk>/attach/", views.AttachDocuments.as_view(), name="attach_documents"),
    path("firearm/<uuid:pk>/", FirearmProductDetails.as_view(), name="firearm_detail"),
    path(
        "components-for-firearms/<uuid:pk>/",
        ComponentsForFirearmsProductDetails.as_view(),
        name="components_for_firearms_detail",
    ),
    path("firearm-ammunition/<uuid:pk>/", FirearmAmmunitionProductDetails.as_view(), name="firearm_ammunition_detail"),
    path(
        "components-for-firearms-ammunition/<uuid:pk>/",
        ComponentsForFirearmsAmmunitionProductDetails.as_view(),
        name="components_for_firearms_ammunition_detail",
    ),
    path("firearms-accessory/<uuid:pk>/", FirearmsAccessoryProductDetails.as_view(), name="firearms_accessory_detail"),
    path(
        "software-related-to-firearms/<uuid:pk>/",
        SoftwareRelatedToFirearmsProductDetails.as_view(),
        name="software_related_to_firearms_detail",
    ),
    path(
        "technology-related-to-firearms/<uuid:pk>/",
        TechnologyRelatedToFirearmsProductDetails.as_view(),
        name="technology_related_to_firearms_detail",
    ),
    path("<uuid:pk>/", views.GoodsDetailEmpty.as_view(), name="good"),
    path("<uuid:pk>/<str:type>/", views.GoodsDetail.as_view(), name="good_detail"),
    path("platform/<uuid:pk>/", CompleteItemProductDetails.as_view(), name="complete_item_detail"),
    path("material/<uuid:pk>/", MaterialProductDetails.as_view(), name="material_detail"),
    path("software/<uuid:pk>/", TechnologyProductDetails.as_view(), name="technology_detail"),
    path("component/<uuid:pk>/", ComponentAccessoryProductDetails.as_view(), name="component_accessory_detail"),
    path(
        "<uuid:pk>/archive-restore/<str:action>/",
        common_views.GoodArchiveRestoreView.as_view(),
        name="good_archive_restore",
    ),
]


if settings.FEATURE_FLAG_FIREARMS_ENABLED:
    urlpatterns += [
        path("<uuid:pk>/<str:type>/<uuid:draft_pk>/", views.GoodsDetail.as_view(), name="good_detail_application"),
        path("<uuid:pk>/edit/application/<uuid:draft_pk>/", views.EditGood.as_view(), name="edit-add-application"),
        path(
            "<uuid:pk>/edit-firearm-details/year-of-manufacture/application/<uuid:draft_pk>/",
            views.EditCalibreView.as_view(),
            name="year-of-manufacture-add-application",
        ),
        path(
            "<uuid:pk>/edit-firearm-details/calibre/application/<uuid:draft_pk>/",
            views.EditCalibreView.as_view(),
            name="calibre-add-application",
        ),
        path(
            "<uuid:pk>/software-technology/application/<uuid:draft_pk>/",
            views.GoodSoftwareTechnologyView.as_view(),
            name="good_software_technology_add_application",
        ),
        path(
            "<uuid:pk>/military-use/application/<uuid:draft_pk>/",
            views.GoodMilitaryUseView.as_view(),
            name="good_military_use_add_application",
        ),
        path(
            "<uuid:pk>/good-component/application/<uuid:draft_pk>/",
            views.GoodComponentView.as_view(),
            name="good_component_add_application",
        ),
        path(
            "<uuid:pk>/information-security/application/<uuid:draft_pk>/",
            views.GoodInformationSecurityView.as_view(),
            name="good_information_security_add_application",
        ),
        path(
            "<uuid:pk>/edit-firearm-details/type/application/<uuid:draft_pk>/",
            views.EditFirearmProductTypeView.as_view(),
            name="firearm_type_add_application",
        ),
        path(
            "<uuid:pk>/edit-firearm-details/firearms-act/application/<uuid:draft_pk>/",
            views.EditFirearmActDetailsView.as_view(),
            name="firearms_act_add_application",
        ),
        path(
            "<uuid:pk>/edit-firearm-details/identification_markings/application/<uuid:draft_pk>/",
            views.EditIdentificationMarkingsView.as_view(),
            name="identification_markings_add_application",
        ),
        path(
            "<uuid:pk>/edit-grading/application/<uuid:draft_pk>/",
            views.EditGrading.as_view(),
            name="edit_grading_add_application",
        ),
        path(
            "<uuid:pk>/add-document/application/<uuid:draft_pk>/",
            views.CheckDocumentGrading.as_view(),
            name="add_document_add_application",
        ),
        path(
            "<uuid:pk>/attach/application/<uuid:draft_pk>/",
            views.AttachDocuments.as_view(),
            name="attach_documents_add_application",
        ),
        path(
            "<uuid:pk>/application/<uuid:draft_pk>/documents/<uuid:file_pk>/delete/",
            views.DeleteDocument.as_view(),
            name="delete_document_add_application",
        ),
    ]
