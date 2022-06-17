from django.urls import path

from exporter.core.constants import Permissions
from exporter.core.helpers import decorate_patterns_with_permission
from exporter.organisation.roles import views

app_name = "roles"
urlpatterns = [
    path("", views.Roles.as_view(), name="roles"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permissions.EXPORTER_ADMINISTER_ROLES)
