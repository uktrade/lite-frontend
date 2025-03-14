from django.urls import path

from . import views

app_name = "supporting_documents"

urlpatterns = [
    path("", views.SupportingDocumentsView.as_view(), name="add"),
    path("attach-document/", views.SupportingDocumentsAddView.as_view(), name="attach"),
]
