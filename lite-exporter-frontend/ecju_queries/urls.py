from django.urls import path

from ecju_queries import views

app_name = "ecju_queries"

urlpatterns = [
    path("<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/",
        views.RespondToQuery.as_view(),
        name="respond_to_query_extra",
    ),
]
