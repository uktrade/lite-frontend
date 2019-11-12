from django.urls import path

from applications.views import goods, documents, third_parties, locations, end_users, additional_documents, common, \
    reference_name, told_by_an_official
from goodstype import views as goodstypeviews


app_name = 'applications'
urlpatterns = [
    path('', common.ApplicationsList.as_view(), name='applications'),
    path('<uuid:pk>/', common.ApplicationDetailEmpty.as_view(), name='application'),
    path('<uuid:pk>/delete/', common.DeleteApplication.as_view(), name='delete'),
    path('<uuid:pk>/edit/', common.ApplicationEditOverview.as_view(), name='edit'),
    path('<uuid:pk>/edit/type/', common.ApplicationEditType.as_view(), name='edit_type'),

    path('<uuid:pk>/edit/reference-name/', reference_name.ApplicationEditReferenceName.as_view(),
         name='edit_reference_name'),
    path('<uuid:pk>/edit/told-by-an-official/', told_by_an_official.ApplicationEditToldByAnOfficial.as_view(),
         name='edit_told_by_an_official'),

    path('<uuid:pk>/ecju-queries/<uuid:query_pk>/', common.RespondToQuery.as_view(), name='respond_to_query'),

    path('<uuid:pk>/open-goods/', goods.DraftOpenGoodsTypeList.as_view(), name='open_goods'),
    path('<uuid:pk>/goods-types/add/', goodstypeviews.ApplicationAddGoodsType.as_view(), name='add_goods_type'),
    path('<uuid:pk>/goods-types/remove/<uuid:goods_type_pk>/', goodstypeviews.ApplicationRemoveGoodsType.as_view(),
         name='remove_goods_type'),
    path('<uuid:pk>/goods/', goods.DraftGoodsList.as_view(), name='goods'),
    path('<uuid:pk>/goods/add-new/', goods.AddNewGood.as_view(), name='new_good'),
    path('<uuid:pk>/goods/add-preexisting/', goods.GoodsList.as_view(), name='preexisting_good'),
    path('<uuid:pk>/goods/add-preexisting/<uuid:good_pk>/add/', goods.AddPreexistingGood.as_view(),
         name='add_preexisting_good'),
    path('<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/remove/', goods.RemovePreexistingGood.as_view(),
         name='remove_preexisting_good'),

    path('<uuid:pk>/location/', locations.Location.as_view(), name='location'),
    path('<uuid:pk>/location/existing-sites/', locations.ExistingSites.as_view(), name='existing_sites'),
    path('<uuid:pk>/location/external-locations/', locations.ExternalLocations.as_view(), name='external_locations'),
    path('<uuid:pk>/location/external-locations/add/', locations.AddExternalLocation.as_view(),
         name='add_external_location'),
    path('<uuid:pk>/location/external-locations/<uuid:ext_loc_pk>', locations.RemoveExternalLocation.as_view(),
         name='remove_external_location'),
    path('<uuid:pk>/location/external-locations/preexisting/', locations.AddExistingExternalLocation.as_view(),
         name='add_preexisting_external_location'),
    path('<uuid:pk>/location/countries/', locations.Countries.as_view(), name='countries'),

    path('<uuid:pk>/end-user/', end_users.EndUser.as_view(), name='end_user'),
    path('<uuid:pk>/end-user/remove', end_users.RemoveEndUser.as_view(), name='remove_end_user'),
    path('<uuid:pk>/end-user/document/attach', documents.AttachDocuments.as_view(), name='end_user_attach_document'),
    path('<uuid:pk>/end-user/document/download', documents.DownloadDocument.as_view(),
         name='end_user_download_document'),
    path('<uuid:pk>/end-user/document/delete', documents.DeleteDocument.as_view(), name="end_user_delete_document"),

    path('<uuid:pk>/consignee/', third_parties.Consignee.as_view(), name='consignee'),
    path('<uuid:pk>/consignee/remove', third_parties.RemoveConsignee.as_view(), name='remove_consignee'),
    path('<uuid:pk>/consignee/document/attach', documents.AttachDocuments.as_view(), name='consignee_attach_document'),
    path('<uuid:pk>/consignee/document/download', documents.DownloadDocument.as_view(),
         name='consignee_download_document'),
    path('<uuid:pk>/consignee/document/delete', documents.DeleteDocument.as_view(), name="consignee_delete_document"),

    path('<uuid:pk>/ultimate-end-users/', end_users.UltimateEndUsers.as_view(), name='ultimate_end_users'),
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/attach', documents.AttachDocuments.as_view(),
         name='ultimate_end_user_attach_document'),
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/download', documents.DownloadDocument.as_view(),
         name='ultimate_end_user_download_document'),
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/delete', documents.DeleteDocument.as_view(),
         name="ultimate_end_user_delete_document"),
    path('<uuid:pk>/ultimate-end-users/add', end_users.AddUltimateEndUser.as_view(), name='add_ultimate_end_user'),
    path('<uuid:pk>/ultimate-end-users/<uuid:ueu_pk>/remove', end_users.RemoveUltimateEndUser.as_view(),
         name='remove_ultimate_end_user'),

    path('<uuid:pk>/third-parties/', third_parties.ThirdParties.as_view(), name='third_parties'),
    path('<uuid:pk>/third-parties/add', third_parties.AddThirdParty.as_view(), name='add_third_party'),
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/attach', documents.AttachDocuments.as_view(),
         name='third_party_attach_document'),
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/download', documents.DownloadDocument.as_view(),
         name='third_party_download_document'),
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/delete', documents.DeleteDocument.as_view(),
         name="third_party_delete_document"),
    path('<uuid:pk>/third-parties/<uuid:ueu_pk>/remove', third_parties.RemoveThirdParty.as_view(),
         name='remove_third_party'),

    path('<uuid:pk>/additional-documents/',
         additional_documents.AdditionalDocuments.as_view(), name='additional_documents'),
    path('<uuid:pk>/additional-document/attach', documents.AttachDocuments.as_view(),
         name='attach_additional_document'),
    path('<uuid:pk>/additional-document/<uuid:doc_pk>/download', documents.DownloadDocument.as_view(),
         name='download_additional_document'),
    path('<uuid:pk>/additional-document/<uuid:doc_pk>/delete', documents.DeleteDocument.as_view(),
         name='delete_additional_document'),

    path('<uuid:pk>/<str:type>/', common.ApplicationDetail.as_view(), name='application-detail'),
]
