from django.urls import path

from teams import views

app_name = "teams"
urlpatterns = [
    path("", views.Team.as_view(), name="team"),
    path("s/", views.TeamsList.as_view(), name="teams"),
    path("s/add", views.AddTeam.as_view(), name="add"),
    path("s/<uuid:pk>", views.TeamDetail.as_view(), name="team"),
    path("s/<uuid:pk>/edit", views.EditTeam.as_view(), name="edit"),
]
