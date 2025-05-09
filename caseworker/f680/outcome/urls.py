from django.urls import path

from caseworker.f680.outcome import views


app_name = "outcome"

urlpatterns = [
    path(
        "decide-outcome/",
        views.DecideOutcome.as_view(),
        name="decide_outcome",
    ),
    path(
        "clear-outcome/<uuid:outcome_id>/",
        views.ClearOutcome.as_view(),
        name="clear_outcome",
    ),
]
