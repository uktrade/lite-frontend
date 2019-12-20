from django.urls import path

from conf.constants import Permissions
from core.helpers import decorate_patterns_with_permission
from sites import views

app_name = "sites"

urlpatterns = [
    path("", views.Sites.as_view(), name="sites"),
    path("new/", views.NewSite.as_view(), name="new"),
    path("<uuid:pk>/", views.ViewSite.as_view(), name="site"),
    path("<uuid:pk>/edit/", views.EditSite.as_view(), name="edit"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permissions.ADMINISTER_SITES)
