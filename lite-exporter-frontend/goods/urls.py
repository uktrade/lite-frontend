from django.urls import path

from . import views

app_name = 'goods'
urlpatterns = [
    # ex: /goods/
    path('', views.Goods.as_view(), name='goods'),
    # ex: /goods/43a88949-5db9-4334-b0cc-044e91827451
    # path('<uuid:pk>', views.case, name='good'),
    # ex: /goods/add/
    path('add/', views.AddGood.as_view(), name='add'),
]
