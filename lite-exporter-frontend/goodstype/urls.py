from django.urls import path

from . import views

app_name = 'goods_type'
urlpatterns = [
    path('<uuid:pk>', views.GoodsType.as_view(), name='goods_type'),
    path('<uuid:pk>/countries/', views.GoodsTypeCountries.as_view(), name='goods_countries'),
    path('add/', views.AddGoodsType.as_view(), name='add'),
]
