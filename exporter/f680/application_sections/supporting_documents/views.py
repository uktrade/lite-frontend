from http import HTTPStatus

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse

from core.decorators import expect_status
from core.helpers import get_document_data

from exporter.applications.services import post_application_supporting_document, delete_additional_document
from exporter.f680.payloads import F680DictPayloadBuilder
from exporter.f680.views import F680FeatureRequiredMixin

from .forms import F680AttachSupportingDocument, F680DeleteSupportingDocument
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
    section = "supporting_documents"
    section_label = "Supporting Documents"

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 document",
        "Unexpected error creating F680 document",
    )
    def post_f680_document(self, data):
        return post_application_supporting_document(self.request, data, self.application_id)

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
        self.post_f680_document(payload)
        self.update_supporting_application_documents()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["back_link_url"] = self.get_success_url()
        return context_data

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 supporting documents",
        "Unexpected error updating F680 supporting documents",
    )
    def update_supporting_application_documents(self):
        self.supporting_documents, _ = self.get_f680_supporting_documents(self.application_id)
        supporting_documents_data = [
            {"id": doc["id"], "file": doc.get("name", ""), "description": doc.get("description", "")}
            for doc in self.supporting_documents["results"]
        ]
        current_application = self.application.get("application", {})
        section_payload = F680DictPayloadBuilder().build(
            self.section, self.section_label, current_application, supporting_documents_data
        )
        return self.patch_f680_application(section_payload)


class SupportingDocumentsDeleteView(F680FeatureRequiredMixin, F680SupportingDocumentsMixin, FormView):
    form_class = F680DeleteSupportingDocument
    template_name = "core/form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.document_id = str(kwargs["document_id"])

    def get_back_link_url(self):
        return reverse("f680:supporting_documents:add", kwargs={"pk": self.application_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_link_url()
        return context

    # @expect_status(
    #     HTTPStatus.OK,
    #     "Error updating F680 supporting documents",
    #     "Unexpected error updating F680 supporting documents",
    # )
    # def update_supporting_application_documents(self):
    #     self.supporting_documents, _ = self.get_f680_supporting_documents(self.application_id)
    #     supporting_documents_data = [
    #         {"id": doc["id"], "file": doc.get("name", ""), "description": doc.get("description", "")}
    #         for doc in self.supporting_documents["results"]
    #     ]
    #     current_application = self.application.get("application", {})
    #     section_payload = F680DictPayloadBuilder().build(
    #         self.section, self.section_label, current_application, supporting_documents_data
    #     )
    #     return self.patch_f680_application(section_payload)

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting supporting document on F680 application",
        "Unexpected error updating F680 application",
    )
    def delete_additional_document(self):
        status_code = delete_additional_document(
            self.request,
            self.application_id,
            self.document_id,
        )

        return {}, status_code

    def form_valid(self, form):
        data = form.cleaned_data
        if data.get("confirm_delete", False):
            # self.update_supporting_application_documents()
            self.delete_additional_document()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "f680:supporting_documents:add",
            kwargs={"pk": self.application_id},
        )
