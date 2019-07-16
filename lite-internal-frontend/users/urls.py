from django.urls import path

from users.views import users, roles

app_name = 'users'
urlpatterns = [
    # ex: /users/
    path('', users.UsersList.as_view(), name='users'),
    # ex: /users/<uuid:pk>/ - Go to a user's profile
    path('<uuid:pk>/', users.ViewUser.as_view(), name='user'),
    # ex: /users/add/
    path('add', users.AddUser.as_view(), name='add'),
    # ex: /users/<uuid:pk>/edit/
    path('<uuid:pk>/edit/', users.EditUser.as_view(), name='edit'),
    # ex: /users/<uuid:pk>/edit/deactivate/
    # ex: /users/<uuid:pk>/edit/reactivate/
    path('<uuid:pk>/edit/<str:status>/', users.ChangeUserStatus.as_view(), name='change_status'),
    # ex: /users/profile/ - Go to signed in user's profile
    path('profile/', users.ViewProfile.as_view(), name='profile'),

    # Roles
    # ex: /users/roles/
    path('roles/', roles.Roles.as_view(), name='roles'),
    # ex: /users/roles/add/
    path('roles/add/', roles.AddRole.as_view(), name='add_role'),
    # ex: /users/roles/<str:pk>/edit/
    path('roles/<str:pk>/edit/', roles.EditRole.as_view(), name='edit_role'),
]