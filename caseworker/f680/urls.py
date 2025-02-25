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
        "recommendation/",
        views.CaseRecommendationView.as_view(),
        name="recommendation",
    ),
]
