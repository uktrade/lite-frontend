from django.urls import include, path

urlpatterns = [
    path('', include('core.urls')),
    path('applications/', include('applications.urls')),
    path('apply-for-a-licence/', include('apply_for_a_licence.urls')),
    path('drafts/', include('drafts.urls')),
    path('goods/', include('goods.urls')),
    path('goodstype/', include('goodstype.urls')),
    path('licences/', include('licences.urls')),
    path('sites/', include('sites.urls')),
    path('users/', include('users.urls')),
]
