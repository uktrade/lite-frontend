from django.urls import path

from caseworker.f680 import views
from caseworker.f680.recommendation import views as recommendation_views


app_name = "f680"

urlpatterns = [
    path(
        "",
        views.CaseDetailView.as_view(),
        name="details",
    ),
    path(
        "recommendation/",
        recommendation_views.CaseRecommendationView.as_view(),
        name="recommendation",
    ),
    path(
        "recommendation/select-recommendation-type/",
        recommendation_views.SelectRecommendationTypeView.as_view(),
        name="select_recommendation_type",
    ),
    path(
        "recommendation/view-my-recommendation/",
        recommendation_views.MyRecommendationView.as_view(),
        name="view_my_recommendation",
    ),
    path(
        "recommendation/approve-all/", recommendation_views.GiveApprovalRecommendationView.as_view(), name="approve_all"
    ),
    path(
        "move-case-forward/",
        views.MoveCaseForward.as_view(),
        name="move_case_forward",
    ),
]
