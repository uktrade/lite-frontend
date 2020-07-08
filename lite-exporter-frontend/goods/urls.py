from django.urls import path

from goods import views

app_name = "goods"
urlpatterns = [
    path("", views.Goods.as_view(), name="goods"),
    path("add/", views.AddGood.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditGood.as_view(), name="edit"),
    path("<uuid:pk>/software-technology/", views.GoodSoftwareTechnology.as_view(), name="good_software_technology"),
    path("<uuid:pk>/military-use/", views.GoodMilitaryUse.as_view(), name="good_military_use"),
    path("<uuid:pk>/good-component/", views.GoodComponent.as_view(), name="good_component"),
    path("<uuid:pk>/information-security/", views.GoodInformationSecurity.as_view(), name="good_information_security"),
    path("<uuid:pk>/edit-grading/", views.EditGrading.as_view(), name="edit_grading"),
    path("<uuid:pk>/edit-firearm-details/type/", views.EditFirearmProductType.as_view(), name="firearm_type"),
    path("<uuid:pk>/edit-firearm-details/ammunition/", views.EditAmmunition.as_view(), name="ammunition"),
    path("<uuid:pk>/edit-firearm-details/firearms-act/", views.EditFirearmActDetails.as_view(), name="firearms_act"),
    path(
        "<uuid:pk>/edit-firearm-details/identification_markings/",
        views.EditIdentificationMarkings.as_view(),
        name="identification_markings",
    ),
    path("<uuid:pk>/delete/", views.DeleteGood.as_view(), name="delete"),
    path("<uuid:pk>/add-document/", views.CheckDocumentGrading.as_view(), name="add_document"),
    path("<uuid:pk>/documents/<uuid:file_pk>/", views.Document.as_view(), name="document"),
    path("<uuid:pk>/documents/<uuid:file_pk>/delete/", views.DeleteDocument.as_view(), name="delete_document"),
    path("<uuid:pk>/attach/", views.AttachDocuments.as_view(), name="attach_documents"),
    path("<uuid:pk>/raise-good-query/", views.RaiseGoodsQuery.as_view(), name="raise_goods_query"),
    path("<uuid:pk>/", views.GoodsDetailEmpty.as_view(), name="good"),
    path("<uuid:pk>/<str:type>/", views.GoodsDetail.as_view(), name="good_detail"),
]
