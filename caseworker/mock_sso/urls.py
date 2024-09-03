from django.urls import path

from core.mock_sso import views


app_name = "mock_sso"

urlpatterns = [
    path("o/authorize/", views.Authorize.as_view(), name="authorize"),
    path("o/token/", views.Token.as_view(), name="token"),
    path("api/v1/user/me/", views.APIUserMe.as_view(), name="api_user_me"),
    path("auth/logout/", views.Logout.as_view(), name="logout"),
]
