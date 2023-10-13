from django.urls import path

from caseworker.tau.views import TAUHome, TAUEdit, TAUMoveCaseForward, TAUClearAssessments, TAUPreviousAssessments

app_name = "tau"

urlpatterns = [
    path("", TAUHome.as_view(), name="home"),
    path("edit/<good_id>", TAUEdit.as_view(), name="edit"),
    path("move-case-forward/", TAUMoveCaseForward.as_view(), name="move_case_forward"),
    path("clear-assessments/", TAUClearAssessments.as_view(), name="clear_assessments"),
    path("previous-assessments/", TAUPreviousAssessments.as_view(), name="previous_assessments"),
]
