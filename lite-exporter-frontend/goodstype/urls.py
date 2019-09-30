from django.urls import path

from . import views

app_name = 'goods_type'
urlpatterns = [
    path('<uuid:pk>/countries/', views.GoodsTypeCountries.as_view(), name='goods_countries'),
]
