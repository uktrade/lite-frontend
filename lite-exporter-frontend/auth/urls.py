from django.urls import path

from auth import views

app_name = "auth"

urlpatterns = [
    path("login/", views.AuthView.as_view(), name="login"),
    path("callback/", views.AuthCallbackView.as_view(), name="callback"),
    path("logout/", views.AuthLogoutView.as_view(), name="logout"),
]
