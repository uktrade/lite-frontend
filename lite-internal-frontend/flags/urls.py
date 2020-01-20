from django.urls import path

from flags import views

app_name = "flags"

urlpatterns = [
    path("", views.FlagsList.as_view(), name="flags"),
    path("add/", views.AddFlag.as_view(), name="add"),
    path("<str:status>/", views.FlagsList.as_view(), name="flags"),
    path("<uuid:pk>/", views.ViewFlag.as_view(), name="flag"),
    path("<uuid:pk>/edit/", views.EditFlag.as_view(), name="edit"),
    path("<uuid:pk>/edit/<str:status>/", views.ChangeFlagStatus.as_view(), name="change_status"),
]
