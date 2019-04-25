from django.urls import path

from . import views

app_name = 'new_application'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /start
    path('start', views.start, name='start'),
    # ex: /form/123 or /form/123?id=abc
    path('form/<uuid:pk>', views.form, name='form'),
    # ex: /draft/overview?id=abc
    path('draft/overview', views.overview, name='overview'),
    # ex: /draft/submit?id=abc
    path('draft/submit', views.submit, name='submit'),
    # ex: /draft/cancel?id=abc
    path('draft/cancel', views.cancel, name='cancel'),
    # ex: /draft/cancel-confirm?id=abc
    path('draft/cancel-confirm', views.cancel_confirm, name='cancel_confirm'),
    # ex: /draft/goods?id=abc
    path('draft/goods', views.goods, name='goods'),
    # ex: /draft/goods/add_preexisting?id=abc
    path('draft/goods/add_preexisting', views.add_preexisting, name='preexisting_good'),
    # ex: /draft/goods/add_preexisting/<uuid:pk>/add/?id=abc
    path('draft/goods/add_preexisting/<uuid:pk>/add/', views.AddPreexistingGood.as_view(), name='add_preexisting_good'),
]
