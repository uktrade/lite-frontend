from django.urls import path

from . import queues

app_name = "api"

urlpatterns = [
    path("teams/<uuid:pk>/queues/", queues.TeamQueuesList.as_view(), name="team-queues"),
]
