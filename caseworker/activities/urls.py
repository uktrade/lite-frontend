from django.urls import path

from . import views


app_name = "activities"

urlpatterns = [
    path(
        "",
        views.NotesAndTimelineAll.as_view(),
        name="notes-and-timeline-all",
    ),
]
