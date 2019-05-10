from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    # ex: /users/
    path('', views.Users.as_view(), name='users'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/ - Go to a user's profile
    path('<uuid:pk>/', views.ViewUser.as_view(), name='user'),
    # ex: /users/add/
    path('add', views.AddUser.as_view(), name='add'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/
    path('<uuid:pk>/edit/', views.EditUser.as_view(), name='edit'),
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/deactivate/
    # ex: /users/43a88949-5db9-4334-b0cc-044e91827451/edit/reactivate/
    path('<uuid:pk>/edit/<str:status>/', views.ChangeUserStatus.as_view(), name='change_status'),
    # ex: /users/profile/ - Go to signed in user's profile
    path('profile/', views.ViewProfile.as_view(), name='profile'),
]
