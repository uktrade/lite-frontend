from django.urls import path

from caseworker.core.constants import Permission
from caseworker.core.helpers import decorate_patterns_with_permission
from caseworker.picklists import views

app_name = "picklists"

urlpatterns = [
    path("", views.Picklists.as_view(), name="picklists"),
    path("<uuid:pk>/", views.ViewPicklistItem.as_view(), name="picklist_item"),
    path("add/", views.AddPicklistItem.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditPicklistItem.as_view(), name="edit"),
    path("<uuid:pk>/<str:status>/", views.ChangeStatusView.as_view(), name="change_status"),
]
decorate_patterns_with_permission(urlpatterns, Permission.MANAGE_PICKLISTS)

urlpatterns += [
    path(".json", views.PicklistsJson.as_view(), name="picklists_json"),
]
