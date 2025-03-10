from http import HTTPStatus

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse

from core.decorators import expect_status
from core.helpers import get_document_data

from exporter.applications.services import post_application_supporting_document
from exporter.f680.views import F680FeatureRequiredMixin

from .forms import F680AttachSupportingDocument
from .mixins import F680SupportingDocumentsMixin


class SupportingDocumentsView(F680FeatureRequiredMixin, F680SupportingDocumentsMixin, TemplateView):
    template_name = "f680/supporting_documents/supporting-documents.html"

    def get_context_data(self, pk, **kwargs):
        return {
            "application": self.application,
            "supporting_documents": self.supporting_documents["results"],
            "back_link_url": reverse(
                "f680:summary",
                kwargs={"pk": self.application_id},
            ),
        }


class SupportingDocumentsAddView(F680FeatureRequiredMixin, F680SupportingDocumentsMixin, FormView):
    form_class = F680AttachSupportingDocument
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 document",
        "Unexpected error creating F680 document",
    )
    def post_f680_document(self, data, application_id):
        return post_application_supporting_document(self.request, data, application_id)

    def get_success_url(self):
        return reverse(
            "f680:supporting_documents:add",
            kwargs={"pk": self.application_id},
        )

    def form_valid(self, form):
        data = form.cleaned_data
        file = data["file"]
        description = data["description"]
        payload = {**get_document_data(file), "description": description, "application": self.application_id}
        self.post_f680_document(payload, self.application_id)
        # TODO After we enrich the JSON with
        # {supporting-documents: {documents:{}}}
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["back_link_url"] = self.get_success_url()
        return context_data
