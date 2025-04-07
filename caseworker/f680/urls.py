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
        "activities/",
        views.NotesAndTimelineView.as_view(),
        name="notes_and_timeline",
    ),
    path(
        "supporting-documents/",
        views.SupportingDocumentsView.as_view(),
        name="supporting_documents",
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
        "recommendation/clear-recommendation/",
        recommendation_views.ClearRecommendationView.as_view(),
        name="clear_recommendation",
    ),
    path(
        "ecju-queries/",
        views.ECJUQueryListView.as_view(),
        name="ecju_queries",
    ),
    path("ecju-queries/new/", views.NewECJUQueryView.as_view(), name="new_ecju_query"),
    path("ecju-queries/<uuid:query_pk>/close-query/", views.CloseECJUQueryView.as_view(), name="close_ecju_query"),
    path(
        "move-case-forward/",
        views.MoveCaseForward.as_view(),
        name="move_case_forward",
    ),
    path("document/", include("caseworker.f680.document.urls")),
    path("outcome/", include("caseworker.f680.outcome.urls")),
]
