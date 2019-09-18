from django.urls import path

from apply_for_a_licence.views import common, locations, end_users, third_parties, documents, goods
from goodstype import views as goodstypeviews

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /
    path('', common.StartApplication.as_view(), name='index'),
    # ex: /start/
    path('start/', common.InitialQuestions.as_view(), name='start'),
    # ex: /<uuid:pk>/overview/
    path('<uuid:pk>/overview/', common.Overview.as_view(), name='overview'),

    # ex: /<uuid:pk/open-goods/
    path('<uuid:pk>/add/open-goods', goodstypeviews.DraftAddGoodsType.as_view(), name='add_open_goods'),
    # ex: /<uuid:pk>/goods/
    path('<uuid:pk>/open-goods/', goods.DraftOpenGoodsTypeList.as_view(), name='open_goods'),
    path('<uuid:pk>/goods/', goods.DraftGoodsList.as_view(), name='goods'),
    # ex: /<uuid:pk>/goods/add-preexisting/
    path('<uuid:pk>/goods/add-preexisting/', goods.GoodsList.as_view(), name='preexisting_good'),
    # ex: /<uuid:pk>/goods/add-preexisting/<uuid:pk>/add/
    path('<uuid:pk>/goods/add-preexisting/<uuid:good_pk>/add/', goods.AddPreexistingGood.as_view(),
         name='add_preexisting_good'),

    # ex: /<uuid:pk>/delete/
    path('<uuid:pk>/delete/', common.DeleteApplication.as_view(), name='delete'),

    # ex: /<uuid:pk>/location/
    path('<uuid:pk>/location/', locations.Location.as_view(), name='location'),
    # ex: /<uuid:pk>/location/existing-sites/
    path('<uuid:pk>/location/existing-sites/', locations.ExistingSites.as_view(), name='existing_sites'),
    # ex: /<uuid:pk>/location/external-locations/
    path('<uuid:pk>/location/external-locations/', locations.ExternalLocations.as_view(), name='external_locations'),
    # ex: /<uuid:pk>/location/external-locations/add/
    path('<uuid:pk>/location/external-locations/add/', locations.AddExternalLocation.as_view(), name='add_external_location'),
    # ex: /<uuid:pk>/location/external-locations/preexisting/
    path('<uuid:pk>/location/external-locations/preexisting/', locations.AddExistingExternalLocation.as_view(), name='add_preexisting_external_location'),
    # ex: /<uuid:pk>/location/countries/
    path('<uuid:pk>/location/countries/', locations.Countries.as_view(), name='countries'),

    # ex: /<uuid:pk>/end-user/
    path('<uuid:pk>/end-user/', end_users.EndUser.as_view(), name='end_user'),
    # ex: /apply_for_a_licence/<uuid:pk>/end-user/attach-document
    path('<uuid:pk>/end-user/document/attach', documents.AttachDocuments.as_view(), name='end_user_attach_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/end-user/download-document/ - Get document
    path('<uuid:pk>/end-user/document/download', documents.DownloadDocument.as_view(), name='end_user_download_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/end-user/download-document/ - Delete a document
    path('<uuid:pk>/end-user/document/delete', documents.DeleteDocument.as_view(), name="end_user_delete_document"),

    # ex: /<uuid:pk>/consignee/
    path('<uuid:pk>/consignee/', third_parties.Consignee.as_view(), name='consignee'),
    # ex: /apply_for_a_licence/<uuid:pk>/consignee/attach-document
    path('<uuid:pk>/consignee/document/attach', documents.AttachDocuments.as_view(), name='consignee_attach_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/consignee/download-document/ - Get documents
    path('<uuid:pk>/consignee/document/download', documents.DownloadDocument.as_view(), name='consignee_download_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/consignee/download-document/ - Delete a document
    path('<uuid:pk>/consignee/document/delete', documents.DeleteDocument.as_view(), name="consignee_delete_document"),

    # ex: /<uuid:pk>/ultimate-end-users/
    path('<uuid:pk>/ultimate-end-users/', end_users.UltimateEndUsers.as_view(), name='ultimate_end_users'),
    # ex: /apply_for_a_licence/<uuid:pk>/ultimate-end-user/attach-document
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/attach', documents.AttachDocuments.as_view(), name='ultimate_end_user_attach_document'),
    # ex: /apply_for_a_licence//<uuid:pk>/ultimate-end-user/download-document/ - Get documents
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/download', documents.DownloadDocument.as_view(), name='ultimate_end_user_download_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/ultimate-end-user/download-document/ - Delete a document
    path('<uuid:pk>/ultimate-end-user/<uuid:ueu_pk>/document/delete', documents.DeleteDocument.as_view(), name="ultimate_end_user_delete_document"),
    # ex: /<uuid:pk>/ultimate-end-users/add
    path('<uuid:pk>/ultimate-end-users/add', end_users.AddUltimateEndUser.as_view(), name='add_ultimate_end_user'),

    # ex: /<uuid:pk>/ultimate-end-users/remove
    path('<uuid:pk>/ultimate-end-users/<uuid:ueu_pk>/remove', end_users.RemoveUltimateEndUser.as_view(), name='remove_ultimate_end_user'),

    # ex: /<uuid:pk>/third-party/
    path('<uuid:pk>/third-parties/', third_parties.ThirdParties.as_view(), name='third_parties'),
    # ex: /<uuid:pk>/third-parties/add
    path('<uuid:pk>/third-parties/add', third_parties.AddThirdParty.as_view(), name='add_third_party'),
    # ex: /apply_for_a_licence/<uuid:pk>/ultimate-end-user/attach-document
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/attach', documents.AttachDocuments.as_view(), name='third_party_attach_document'),
    # ex: /apply_for_a_licence//<uuid:pk>/ultimate-end-user/download-document/ - Get documents
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/download', documents.DownloadDocument.as_view(), name='third_party_download_document'),
    # ex: /apply_for_a_licence/<uuid:pk>/ultimate-end-user/download-document/ - Delete a document
    path('<uuid:pk>/third-parties/<uuid:tp_pk>/document/delete', documents.DeleteDocument.as_view(), name="third_party_delete_document"),
    # ex: /<uuid:pk>/third-parties/remove
    path('<uuid:pk>/third-parties/<uuid:ueu_pk>/remove', third_parties.RemoveThirdParty.as_view(), name='remove_third_party')
]
