from django.urls import path

from applications.views import goods, documents, third_parties, locations, end_users, additional_documents, common, \
    reference_name, told_by_an_official
from goodstype import views as goodstypeviews


app_name = 'applications'
urlpatterns = [
    # ex: /applications/
    path('', common.ApplicationsList.as_view(), name='applications'),
    # ex: /applications/<uuid:pk>/
    path('<uuid:pk>/', common.ApplicationDetailEmpty.as_view(), name='application'),
    # ex: /<uuid:pk>/delete/
    path('<uuid:pk>/delete/', common.DeleteApplication.as_view(), name='delete'),
    # ex: /applications/<uuid:pk>/edit/
    path('<uuid:pk>/edit/', common.ApplicationEditOverview.as_view(), name='edit'),
    # ex: /applications/<uuid:pk>/edit/type/
    path('<uuid:pk>/edit/type/', common.ApplicationEditType.as_view(), name='edit_type'),

    # ex: /applications/<uuid:pk>/edit/reference-name/
    path('<uuid:pk>/edit/reference-name/', reference_name.ApplicationEditReferenceName.as_view(),
         name='edit_reference_name'),
    # ex: /applications/<uuid:pk>/edit/told-by-an-official/
    path('<uuid:pk>/edit/told-by-an-official/', told_by_an_official.ApplicationEditToldByAnOfficial.as_view(),
         name='edit_told_by_an_official'),

    # ex: /applications/<uuid:pk>/
    path('<uuid:pk>/ecju-queries/<uuid:query_pk>/', common.RespondToQuery.as_view(), name='respond_to_query'),

    # ex: /applications/<uuid:pk>/open-goods/
    path('<uuid:pk>/open-goods/', goods.DraftOpenGoodsTypeList.as_view(), name='open_goods'),
    # ex: /applications/<uuid:pk>/open-goods/add/
    path('<uuid:pk>/goods-types/add/', goodstypeviews.ApplicationAddGoodsType.as_view(), name='add_goods_type'),
    # ex: /applications/<uuid:pk>/open-goods/remove/<uuid:goods_type_pk>/
    path('<uuid:pk>/goods-types/remove/<uuid:goods_type_pk>/', goodstypeviews.ApplicationRemoveGoodsType.as_view(),
         name='remove_goods_type'),
    # ex: /applications/<uuid:pk>/goods/
    path('<uuid:pk>/goods/', goods.DraftGoodsList.as_view(), name='goods'),
    # ex: /applications/<uuid:pk>/goods/add-preexisting/
    path('<uuid:pk>/goods/add-preexisting/', goods.GoodsList.as_view(), name='preexisting_good'),
    # ex: /applications/<uuid:pk>/goods/add-preexisting/<uuid:pk>/add/
    path('<uuid:pk>/goods/add-preexisting/<uuid:good_pk>/add/', goods.AddPreexistingGood.as_view(),
         name='add_preexisting_good'),
    # ex: /applications/<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/remove/
    path('<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/remove/', goods.RemovePreexistingGood.as_view(),
         name='remove_preexisting_good'),

    # ex: /<uuid:pk>/location/
    path('<uuid:pk>/location/', locations.Location.as_view(), name='location'),
    # ex: /<uuid:pk>/location/existing-sites/
    path('<uuid:pk>/location/existing-sites/', locations.ExistingSites.as_view(), name='existing_sites'),
    # ex: /<uuid:pk>/location/external-locations/
    path('<uuid:pk>/location/external-locations/', locations.ExternalLocations.as_view(), name='external_locations'),
    # ex: /<uuid:pk>/location/external-locations/add/
    path('<uuid:pk>/location/external-locations/add/', locations.AddExternalLocation.as_view(),
         name='add_external_location'),
    # ex: /<uuid:pk>/location/external-locations/<uuid:ext_loc_pk>
    path('<uuid:pk>/location/external-locations/<uuid:ext_loc_pk>', locations.RemoveExternalLocation.as_view(),
         name='remove_external_location'),
    # ex: /<uuid:pk>/location/external-locations/preexisting/
    path('<uuid:pk>/location/external-locations/preexisting/', locations.AddExistingExternalLocation.as_view(),
         name='add_preexisting_external_location'),
    # ex: /<uuid:pk>/location/countries/
    path('<uuid:pk>/location/countries/', locations.Countries.as_view(), name='countries'),

    # ex: /<uuid:pk>/end-user/
    path('<uuid:pk>/end-user/', end_users.EndUser.as_view(), name='end_user'),
    # ex: /<uuid:pk>/end-user/remove
    path('<uuid:pk>/end-user/remove', end_users.RemoveEndUser.as_view(), name='remove_end_user'),
    # ex: /applications/<uuid:pk>/end-user/attach-document
    path('<uuid:pk>/end-user/document/attach', documents.AttachDocuments.as_view(), name='end_user_attach_document'),
    # ex: /applications/<uuid:pk>/end-user/download-document/ - Get document
    path('<uuid:pk>/end-user/document/download', documents.DownloadDocument.as_view(),
         name='end_user_download_document'),
    # ex: /applications/<uuid:pk>/end-user/download-document/ - Delete a document
    path('<uuid:pk>/end-user/document/delete', documents.DeleteDocument.as_view(), name="end_user_delete_document"),

    # ex: /<uuid:pk>/consignee/
    path('<uuid:pk>/consignee/', third_parties.Consignee.as_view(), name='consignee'),
    # ex: /<uuid:pk>/consignee/remove/
    path('<uuid:pk>/consignee/remove', third_parties.RemoveConsignee.as_view(), name='remove_consignee'),
    # ex: /applications/<uuid:pk>/consignee/attach-document
    path('<uuid:pk>/consignee/document/attach', documents.AttachDocuments.as_view(), name='consignee_attach_document'),
    # ex: /applications/<uuid:pk>/consignee/download-document/ - Get documents
    path('<uuid:pk>/consignee/document/download', documents.DownloadDocument.as_view(),
         name='consignee_download_document'),
    # ex: /applications/<uuid:pk>/consignee/download-document/ - Delete a document
    path('<uuid:pk>/consignee/document/delete', documents.DeleteDocument.as_view(), name="consignee_delete_document"),

    # ex: /<uuid:pk>/ultimate-end-users/
    path('<uuid:pk>/ultimate-end-users/', end_users.UltimateEndUsers.as_view(), name='ultimate_end_users'),
    # ex: /applications/<uuid:pk>/ultimate-end-user/attach-document
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/attach', documents.AttachDocuments.as_view(),
         name='ultimate_end_user_attach_document'),
    # ex: /applications/<uuid:pk>/ultimate-end-user/download-document/ - Get documents
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/download', documents.DownloadDocument.as_view(),
         name='ultimate_end_user_download_document'),
    # ex: /applications/<uuid:pk>/ultimate-end-user/download-document/ - Delete a document
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/delete', documents.DeleteDocument.as_view(),
         name="ultimate_end_user_delete_document"),
    # ex: /<uuid:pk>/ultimate-end-users/add
    path('<uuid:pk>/ultimate-end-users/add', end_users.AddUltimateEndUser.as_view(), name='add_ultimate_end_user'),
    # ex: /<uuid:pk>/ultimate-end-users/remove
    path('<uuid:pk>/ultimate-end-users/<uuid:ueu_pk>/remove', end_users.RemoveUltimateEndUser.as_view(),
         name='remove_ultimate_end_user'),

    # ex: /<uuid:pk>/third-parties/
    path('<uuid:pk>/third-parties/', third_parties.ThirdParties.as_view(), name='third_parties'),
    # ex: /<uuid:pk>/third-parties/add
    path('<uuid:pk>/third-parties/add', third_parties.AddThirdParty.as_view(), name='add_third_party'),
    # ex: /applications/<uuid:pk>/ultimate-end-user/attach-document
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/attach', documents.AttachDocuments.as_view(),
         name='third_party_attach_document'),
    # ex: /applications//<uuid:pk>/ultimate-end-user/download-document/ - Get documents
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/download', documents.DownloadDocument.as_view(),
         name='third_party_download_document'),
    # ex: /applications/<uuid:pk>/ultimate-end-user/download-document/ - Delete a document
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/delete', documents.DeleteDocument.as_view(),
         name="third_party_delete_document"),
    # ex: /<uuid:pk>/third-parties/remove
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

    # ex: /applications/<uuid:pk>/case-notes/
    path('<uuid:pk>/<str:type>/', common.ApplicationDetail.as_view(), name='application-detail'),
]
