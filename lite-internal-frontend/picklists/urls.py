from django.urls import path

from conf.constants import Permission
from core.helpers import decorate_patterns_with_permission
from picklists import views

app_name = "picklists"

urlpatterns = [
    path("", views.Picklists.as_view(), name="picklists"),
    path(".json", views.PicklistsJson.as_view(), name="picklists_json"),
    path("<uuid:pk>/", views.ViewPicklistItem.as_view(), name="picklist_item"),
    path("add/", views.AddPicklistItem.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditPicklistItem.as_view(), name="edit"),
    path("<uuid:pk>/edit/deactivate/", views.DeactivatePicklistItem.as_view(), name="deactivate"),
    path("<uuid:pk>/edit/reactivate/", views.ReactivatePicklistItem.as_view(), name="reactivate"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permission.MANAGE_PICKLISTS)
