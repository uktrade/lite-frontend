from django.urls import path

from caseworker.tau.views import (
    TAUHome,
    TAUMoveCaseForward,
    TAUClearAssessments,
    TAUPreviousAssessments,
    TAUMultipleEdit,
    TAUChooseAssessmentEdit,
)

app_name = "tau"

urlpatterns = [
    path("", TAUHome.as_view(), name="home"),
    path("move-case-forward/", TAUMoveCaseForward.as_view(), name="move_case_forward"),
    path("clear-assessments/", TAUClearAssessments.as_view(), name="clear_assessments"),
    path("previous-assessments/", TAUPreviousAssessments.as_view(), name="previous_assessments"),
    path("multiple-edit/", TAUMultipleEdit.as_view(), name="multiple_edit"),
    path("multiple-edit-choice/", TAUChooseAssessmentEdit.as_view(), name="choose_multiple_edit"),
]
