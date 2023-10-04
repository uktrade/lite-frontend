from django.urls import path

from core.mock_sso import views


app_name = "mock_sso"

urlpatterns = [
    path("authorize/", views.Authorize.as_view(), name="authorize"),
    path("token/", views.Token.as_view(), name="token"),
    path("userinfo/", views.UserInfo.as_view(), name="userinfo"),
    # api_user_me is legacy, enabled here for unit tests.
    path("api/v1/user/me/", views.APIUserMe.as_view(), name="api_user_me"),
]
