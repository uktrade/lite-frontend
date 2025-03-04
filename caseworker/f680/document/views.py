from http import HTTPStatus
from urllib.parse import quote

from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from caseworker.cases.services import get_generated_document_preview, post_generated_document
from caseworker.letter_templates.services import get_letter_templates_list

from caseworker.f680.views import F680CaseworkerMixin

from .forms import GenerateDocumentForm, DocumentGenerationForm


class DocumentGenerationView(LoginRequiredMixin, F680CaseworkerMixin, FormView):
    form_class = DocumentGenerationForm
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error getting letter templates",
        "Unexpected error letter templates",
    )
    def get_letter_templates_list(self, filter):
        return get_letter_templates_list(self.request, filter)

    def get_form_kwargs(self):
        # We will pull the decision from the case when filtering
        filter = {"case_type": self.case.case_type["sub_type"]["key"], "decision": "approve"}
        letter_templates, _ = self.get_letter_templates_list(filter)
        form_kwargs = super().get_form_kwargs()
        form_kwargs["approval_templates"] = letter_templates["results"]
        return form_kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        context_data["back_link_url"] = self.get_success_url()
        return context_data

    def get_success_url(self):
        return reverse("cases:f680:details", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})


class F680GenerateDocument(LoginRequiredMixin, F680CaseworkerMixin, FormView):
    template_name = "f680/document/preview.html"
    form_class = GenerateDocumentForm

    @expect_status(
        HTTPStatus.OK,
        "Error generating document preview",
        "Unexpected error generating document preview",
        reraise_404=True,
    )
    def get_generated_document_preview(self, template_id, text):
        # TODO: Use of get_generated_document_preview service helper should
        #   be replaced with something that doesn't require text to be quoted
        return get_generated_document_preview(
            self.request, self.case_id, template=template_id, text=text, addressee=None
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error generating document",
        "Unexpected error generating document",
    )
    def generate_document(self, template_id, text):
        return None, post_generated_document(
            self.request,
            self.case_id,
            {
                "template": template_id,
                "text": text,
                "addressee": None,
                "visible_to_exporter": False,
            },
        )

    def form_valid(self, form):
        if "generate" not in self.request.POST:
            # Just show the preview screen again if the user has clicked preview
            return self.form_invalid(form)

        # TODO: Think about a payload builder
        self.generate_document(str(self.kwargs["template_id"]), form.cleaned_data["text"])
        success_message = "Generated document successfully"
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        # TODO: Redirect the user to the landing screen when we have a document
        return reverse("cases:f680:details", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})

    def get_text(self, form):
        text = None
        if form.is_bound:
            text = quote(form.cleaned_data.get("text", ""))
        return text

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        template_id = str(self.kwargs["template_id"])
        form = context_data["form"]
        text = self.get_text(form)
        preview_response, _ = self.get_generated_document_preview(template_id=template_id, text=text)
        context_data.update(
            {
                "preview": preview_response["preview"],
            }
        )
        return context_data
