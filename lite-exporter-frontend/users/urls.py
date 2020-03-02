from django.urls import path

from conf.constants import Permissions
from core.helpers import decorate_patterns_with_permission
from users import views

app_name = "users"

urlpatterns = [
    path("", views.Users.as_view(), name="users"),
    path("<uuid:pk>/", views.ViewUser.as_view(), name="user"),
    path("add/", views.AddUser.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditUser.as_view(), name="edit"),
    path("<uuid:pk>/edit/<str:status>/", views.ChangeUserStatus.as_view(), name="change_status"),
    path("<uuid:pk>/assign-sites/", views.AssignSites.as_view(), name="assign_sites"),
    path("me/", views.ViewProfile.as_view(), name="profile"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permissions.ADMINISTER_USERS, ignore=["user", "profile"])
