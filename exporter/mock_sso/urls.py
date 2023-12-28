from django.urls import path

from core.mock_sso import views
from .views import Logout


app_name = "mock_sso"

urlpatterns = [
    path("authorize", views.Authorize.as_view(), name="authorize"),
    # path("token", views.Token.as_view(), name="token"),
    path("userinfo", views.APIUserMe.as_view(), name="api_user_me"),
    path("logout", Logout.as_view(), name="logout"),
]
