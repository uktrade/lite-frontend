from django.urls import path

from core.auth.views import AuthLogoutView
from exporter.auth import views

app_name = "auth"

urlpatterns = [
    path("login/", views.AuthView.as_view(), name="login"),
    path("callback/", views.AuthCallbackView.as_view(), name="callback"),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
]
