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
]
