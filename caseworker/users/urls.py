from django.urls import path

from caseworker.users.views import users, roles
from caseworker.users.manage import views

app_name = "users"

urlpatterns = [
    path("", users.UsersList.as_view(), name="users"),
    path("<uuid:pk>/", users.ViewUser.as_view(), name="user"),
    path("add", users.AddUser.as_view(), name="add"),
    path("<uuid:pk>/edit/", users.EditUser.as_view(), name="edit"),
    path("<uuid:pk>/edit2/", views.EditCaseworkerUserView.as_view(), name="edit2"),
    path("<uuid:pk>/edit/<str:status>/", users.ChangeUserStatus.as_view(), name="change_status"),
    path("profile/", users.ViewProfile.as_view(), name="profile"),
    path("mentions/", users.UserCaseNoteMentions.as_view(), name="user_case_note_mentions"),
    # Roles
    path("roles/", roles.Roles.as_view(), name="roles"),
    path("roles/add/", roles.AddRole.as_view(), name="add_role"),
    path("roles/<str:pk>/edit/", roles.EditRole.as_view(), name="edit_role"),
]
