from django.urls import path
from apply_for_a_licence.views import common, locations
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
    path('<uuid:pk>/open-goods/', common.DraftOpenGoodsTypeList.as_view(), name='open_goods'),
    path('<uuid:pk>/goods/', common.DraftGoodsList.as_view(), name='goods'),
    # ex: /<uuid:pk>/goods/add-preexisting/
    path('<uuid:pk>/goods/add-preexisting/', common.GoodsList.as_view(), name='preexisting_good'),
    # ex: /<uuid:pk>/goods/add-preexisting/<uuid:pk>/add/
    path('<uuid:pk>/goods/add-preexisting/<uuid:good_pk>/add/', common.AddPreexistingGood.as_view(),
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
    path('<uuid:pk>/end-user/', common.EndUser.as_view(), name='end_user'),
]
