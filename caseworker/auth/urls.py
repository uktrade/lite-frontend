from django.urls import path

import core.auth.views
import caseworker.auth.views

app_name = "auth"

urlpatterns = [
    path("login/", core.auth.views.AuthView.as_view(), name="login"),
    path("callback/", caseworker.auth.views.AuthCallbackView.as_view(), name="callback"),
    path("logout/", core.auth.views.AuthLogoutView.as_view(), name="logout"),
]
