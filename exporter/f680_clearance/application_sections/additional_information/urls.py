from django.urls import path

from . import views


app_name = "additional_information"

urlpatterns = [
    path("notes/", views.NotesForCaseOfficersView.as_view(), name="notes_wizard"),
]
