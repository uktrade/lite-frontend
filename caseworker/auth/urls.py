from django.urls import path

import core.auth.views
from caseworker.auth import views

app_name = "auth"

urlpatterns = [
    path("login/", views.AuthView.as_view(), name="login"),
    path("callback/", views.AuthCallbackView.as_view(), name="callback"),
    path("logout/", core.auth.views.AuthLogoutView.as_view(), name="logout"),
]
