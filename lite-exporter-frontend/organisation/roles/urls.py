from django.urls import path

from conf.constants import Permissions
from core.helpers import decorate_patterns_with_permission
from organisation.roles import views

app_name = "roles"
urlpatterns = [
    path("", views.Roles.as_view(), name="roles"),
    path("new/", views.AddRole.as_view(), name="new"),
    path("<uuid:pk>/edit/", views.EditRole.as_view(), name="edit"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permissions.EXPORTER_ADMINISTER_ROLES)
