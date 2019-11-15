from django.urls import path

from picklists import views

app_name = "picklists"
urlpatterns = [
    # ex: /picklists/ - View all active picklists
    path("", views.Picklists.as_view(), name="picklists"),
    # ex: /picklists/<uuid:pk>/ - View a picklist item
    path("<uuid:pk>/", views.ViewPicklistItem.as_view(), name="picklist_item"),
    # ex: /picklist/add/ -  Add a new picklist item
    path("add/", views.AddPicklistItem.as_view(), name="add"),
    # ex: /picklists/<uuid:pk>/edit/ - Edit a picklist item
    path("<uuid:pk>/edit/", views.EditPicklistItem.as_view(), name="edit"),
    # ex: /picklists/<uuid:pk>/edit/deactivate/ - Deactivate a picklist item
    path("<uuid:pk>/edit/deactivate/", views.DeactivatePicklistItem.as_view(), name="deactivate"),
    # ex: /picklists/<uuid:pk>/edit/reactivate/ - Reactivate a picklist item
    path("<uuid:pk>/edit/reactivate/", views.ReactivatePicklistItem.as_view(), name="reactivate"),
]
