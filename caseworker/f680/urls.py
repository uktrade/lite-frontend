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
]
