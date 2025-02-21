from http import HTTPStatus

from django.views.generic import TemplateView
from django.urls import reverse

from core.decorators import expect_status

from core.helpers import get_document_data
from exporter.f680.views import F680FeatureRequiredMixin
from exporter.f680.services import get_f680_application, get_f680_documents, post_f680_document
from django.views.generic import FormView

from .forms import F680AttachSupportingDocument


class SupportingDocumentsView(F680FeatureRequiredMixin, TemplateView):
    template_name = "f680/supporting_documents/supporting-documents-documents.html"

    @expect_status(
        HTTPStatus.OK,
        "Error getting F680 documents",
        "Unexpected error getting F680 documents",
        reraise_404=True,
    )
    def get_f680_supporting_documents(self, application_id):
        # A new F680 Endpoint which retrieved all the documents from
        # Application document
        # We could then potentially filter based on what's in the supporting-section
        # Of the JSON however this isn't nesseasry for first parse since we only have supporting
        # documents
        return get_f680_documents(self.request, application_id)

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving F680 application",
        "Unexpected error retrieving F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, pk):
        return get_f680_application(self.request, pk)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])
        self.supporting_documents, _ = self.get_f680_supporting_documents(self.kwargs["pk"])

    def get_context_data(self, pk, **kwargs):
        return {
            "application": self.application,
            "additional_documents": self.supporting_documents["documents"],
        }


class SupportingDocumentsAddView(F680FeatureRequiredMixin, FormView):
    form_class = F680AttachSupportingDocument
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 document",
        "Unexpected error creating F680 document",
    )
    def post_f680_document(self, data):
        return post_f680_document(self.request, data)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])

    def get_success_url(self):
        return reverse(
            "f680:summary",
            kwargs={
                "pk": self.application.id,
            },
        )

    def form_valid(self, form):
        data = form.cleaned_data
        file = data["file"]
        description = data["description"]
        payload = {**get_document_data(file), "description": description, "application": self.application.id}
        # Here we post the document to a new F680 Specific endpoint
        # This is stored on ApplicationDocumention
        # This is required so we can do virus scans etc etc
        self.post_f680_document(payload)
        # After we enrich the JSON with
        # {:supporting-documents: {documents:{}}}
        # This could contain a dummy id for the entry and JSON blurb of the
        # Form i.e in this case description and a reference to the id of the
        # Physical document on ApplicationDocument
        return super().form_valid(form)
