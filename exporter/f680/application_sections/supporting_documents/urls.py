from django.urls import path

from . import views

app_name = "supporting_documents"

urlpatterns = [
    path("", views.SupportingDocumentsView.as_view(), name="add"),
    path("attach-document/", views.SupportingDocumentsAddView.as_view(), name="attach"),
    path("<uuid:document_id>/delete/", views.SupportingDocumentsDeleteView.as_view(), name="delete"),
]
