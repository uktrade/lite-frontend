from django.urls import path

from . import views


app_name = "activities"

urlpatterns = [
    path(
        "",
        views.NotesAndTimeline.as_view(),
        name="notes-and-timeline",
    ),
]
