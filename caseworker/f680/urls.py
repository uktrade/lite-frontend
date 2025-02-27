from django.urls import path

from caseworker.f680 import views


app_name = "f680"

urlpatterns = [
    path(
        "",
        views.CaseDetailView.as_view(),
        name="details",
    ),
    path(
        "move-case-forward",
        views.MoveCaseForward.as_view(),
        name="move_case_forward",
    ),
]
