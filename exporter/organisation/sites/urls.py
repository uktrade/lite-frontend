from django.urls import path

from exporter.core.constants import Permissions
from exporter.core.helpers import decorate_patterns_with_permission
from exporter.organisation.sites import views

app_name = "sites"

urlpatterns = [
    path("", views.Sites.as_view(), name="sites"),
    path("new/", views.NewSite.as_view(), name="new"),
    path("<uuid:pk>/", views.ViewSite.as_view(), name="site"),
    path("<uuid:pk>/edit-name/", views.EditSiteName.as_view(), name="edit_name"),
    path(
        "<uuid:pk>/edit-site-records-location/",
        views.EditSiteRecordsLocation.as_view(),
        name="edit_site_records_location",
    ),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permissions.ADMINISTER_SITES)
