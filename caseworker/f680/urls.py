from django.urls import include, path

from caseworker.f680 import views
from caseworker.f680.recommendation import views as recommendation_views


app_name = "f680"

urlpatterns = [
    path(
        "",
        views.CaseSummaryView.as_view(),
        name="summary",
    ),
    path(
        "details/",
        views.CaseDetailView.as_view(),
        name="details",
    ),
    path(
        "recommendation/",
        recommendation_views.CaseRecommendationView.as_view(),
        name="recommendation",
    ),
    path(
        "recommendation/view-my-recommendation/",
        recommendation_views.MyRecommendationView.as_view(),
        name="view_my_recommendation",
    ),
    path(
        "recommendation/make-recommendation/",
        recommendation_views.MakeRecommendationView.as_view(),
        name="make_recommendation",
    ),
    path(
        "move-case-forward/",
        views.MoveCaseForward.as_view(),
        name="move_case_forward",
    ),
    path("document/", include("caseworker.f680.document.urls")),
]
