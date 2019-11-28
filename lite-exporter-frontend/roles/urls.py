from django.urls import path

from roles import views

app_name = "roles"
urlpatterns = [
    path("", views.Roles.as_view(), name="roles"),
    path("new/", views.AddRole.as_view(), name="new"),
    path("<uuid:pk>/edit/", views.EditRole.as_view(), name="edit"),
]
