from django.views.generic import TemplateView

from exporter.applications.services import get_additional_documents

from core.auth.views import LoginRequiredMixin


class AdditionalDocuments(LoginRequiredMixin, TemplateView):
    template_name = "applications/additional-documents/additional-documents.html"

    def get_context_data(self, **kwargs):
        data, _ = get_additional_documents(self.request, self.kwargs["pk"])
        return super().get_context_data(
            additional_documents=data["documents"],
            application_id=self.kwargs["pk"],
            editable=data["editable"],
            **kwargs,
        )
