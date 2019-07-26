import django

try:
    from django.urls import path
except ImportError:
    from django.conf.urls import url

from .views import AuthView, AuthCallbackView

app_name = 'authbroker_client'

if django.VERSION[0] >= 2:
    urlpatterns = [
        path('login/', AuthView.as_view(), name='login'),
        path('callback/', AuthCallbackView.as_view(), name='callback'),
    ]
else:
    urlpatterns = [
        url('^login/', AuthView.as_view(), name='login'),
        url('^callback/', AuthCallbackView.as_view(), name='callback'),
    ]
