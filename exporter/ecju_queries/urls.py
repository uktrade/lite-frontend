from django.urls import path

from exporter.ecju_queries import views
from exporter.ecju_queries.new_views.ecju_views import ECJURespondQueryView, ECJURespondQueryConfirmView

app_name = "ecju_queries"

urlpatterns = [
    # This superceeds the view respond_to_query where object type is application for other object types we will need to revert to the old view
    path(
        "<uuid:query_pk>/application/<uuid:case_pk>/",
        ECJURespondQueryView.as_view(),
        name="respond_to_application_query",
    ),
    path("<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
    path(
        "<uuid:query_pk>/<uuid:case_pk>/confirm/",
        ECJURespondQueryConfirmView.as_view(),
        name="respond_to_application_query_confirm",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/",
        views.RespondToQuery.as_view(),
        name="respond_to_query_extra",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/add-document/",
        views.UploadDocuments.as_view(),
        name="add_supporting_document",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/document/<uuid:doc_pk>",
        views.QueryDocument.as_view(),
        name="query-document",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/document/<uuid:doc_pk>/delete/",
        views.QueryDocumentDelete.as_view(),
        name="query-document-delete",
    ),
]
