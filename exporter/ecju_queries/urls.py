from django.urls import path

from exporter.ecju_queries import views

app_name = "ecju_queries"

urlpatterns = [
    path("<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/",
        views.RespondToQuery.as_view(),
        name="respond_to_query_extra",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:extra_pk>/case/<uuid:case_pk>/add-document/",
        views.CheckDocumentGrading.as_view(),
        name="add_supporting_document",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/upload-document/",
        views.UploadDocuments.as_view(),
        name="upload_document",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/document/<uuid:doc_pk>",
        views.QueryDocument.as_view(),
        name="query-document",
    ),
    path(
        "<uuid:query_pk>/<str:object_type>/<uuid:case_pk>/document/<uuid:doc_pk>/delete/",
        views.QueryDocumentDelete.as_view(),
        name="query-document-delete",
    ),
]
