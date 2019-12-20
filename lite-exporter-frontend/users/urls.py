from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("", views.Users.as_view(), name="users"),
    path("<uuid:pk>/", views.ViewUser.as_view(), name="user"),
    path("add/", views.AddUser.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditUser.as_view(), name="edit"),
    path("<uuid:pk>/edit/<str:status>/", views.ChangeUserStatus.as_view(), name="change_status"),
    path("profile/", views.ViewProfile.as_view(), name="profile"),
    path("<uuid:pk>/assign-sites/", views.AssignSites.as_view(), name="assign_sites"),
]
