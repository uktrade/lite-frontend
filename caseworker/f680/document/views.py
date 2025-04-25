from http import HTTPStatus

from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.http import Http404
import rules

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from caseworker.cases.services import get_generated_document_preview, post_generated_document, finalise_case
from caseworker.core.views import handler403
from caseworker.letter_templates.services import get_letter_templates_list

from caseworker.f680.outcome.services import get_outcome_documents, get_outcome_documents_templated_list, get_outcomes
from caseworker.f680.views import F680CaseworkerMixin

from .forms import GenerateDocumentForm, FinaliseForm


class F680DocumentMixin(F680CaseworkerMixin):

    def test_func(self):
        return all([super().test_func(), rules.test_rule("can_user_make_f680_outcome_letter", self.request, self.case)])

    def handle_no_permission(self):
        return handler403(self.request, HttpResponseForbidden)

    @expect_status(
        HTTPStatus.OK,
        "Error getting letter templates",
        "Unexpected error letter templates",
    )
    def get_letter_templates_list(self, filter):
        return get_letter_templates_list(self.request, filter)

    @expect_status(
        HTTPStatus.OK,
        "Error getting outcome documents",
        "Unexpected error outcome documents",
    )
    def get_outcome_documents(self, case_id):
        return get_outcome_documents(self.request, case_id)

    def get_case_letter_templates(self):
        """Return letter templates that correspond to the case outcomes"""
        outcomes, _ = get_outcomes(self.request, self.case.id)
        decisions = list({item["outcome"] for item in outcomes})
        filters = {"case_type": self.case.case_type["sub_type"]["key"], "decision": decisions}
        f680_letter_templates, _ = self.get_letter_templates_list(filters)
        return f680_letter_templates

    def get_outcome_templated_documents(self):
        letter_templates = self.get_case_letter_templates()
        outcome_documents, _ = self.get_outcome_documents(self.case_id)
        return get_outcome_documents_templated_list(letter_templates, outcome_documents)


class AllDocuments(LoginRequiredMixin, F680DocumentMixin, FormView):
    form_class = FinaliseForm
    template_name = "f680/document/all_documents.html"
    current_tab = "recommendations"

    @expect_status(
        HTTPStatus.CREATED,
        "Error finalising case",
        "Unexpected error finalising case",
    )
    def finalise(self):
        return finalise_case(self.request, self.case["id"], json={})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["outcome_template_documents"] = self.get_outcome_templated_documents()
        context_data["back_link_url"] = reverse(
            "cases:f680:recommendation", kwargs={"pk": self.case_id, "queue_pk": self.queue_id}
        )
        return context_data

    def form_valid(self, form):
        if self.get_outcomes_templates_with_no_documents():
            form.add_error(
                None,
                [
                    "Click generate for all letters. Finalise and publish to exporter can only be done once all letters have been generated."
                ],
            )
            return super().form_invalid(form)
        self.finalise()
        success_message = "F680 finalised successfully"
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:f680:details", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})

    def get_outcomes_templates_with_no_documents(self):
        get_outcome_templated_documents = self.get_outcome_templated_documents()
        return [t for t in get_outcome_templated_documents if t.get("document") is None]


class F680GenerateDocument(LoginRequiredMixin, F680DocumentMixin, FormView):
    template_name = "f680/core/base_form.html"
    form_class = GenerateDocumentForm
    current_tab = "recommendations"

    @expect_status(
        HTTPStatus.OK,
        "Error generating document preview",
        "Unexpected error generating document preview",
        reraise_404=True,
    )
    def get_generated_document_preview(self, template_id):
        # TODO: Use of get_generated_document_preview service helper should
        #   be replaced with something that doesn't require text to be quoted
        return get_generated_document_preview(
            self.request, self.case_id, template=template_id, text=None, addressee=None
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error generating document",
        "Unexpected error generating document",
    )
    def generate_document(self, template_id):
        advice_type = None
        template_decisions = [decision["name"]["key"] for decision in self.template["decisions"]]
        if "approve" in template_decisions:
            advice_type = "approve"
        if "refuse" in template_decisions:
            advice_type = "refuse"
        return None, post_generated_document(
            self.request,
            self.case_id,
            {
                "template": template_id,
                "addressee": None,
                "visible_to_exporter": False,
                "advice_type": advice_type,
            },
        )

    def extra_setup(self, request):
        super().extra_setup(request)
        template_id = str(self.kwargs["template_id"])
        # Check to see if the letter template being generated is permissible
        try:
            self.template = [t for t in self.get_case_letter_templates() if t["id"] == template_id][0]
        except IndexError:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = self.get_success_url()
        return kwargs

    def form_valid(self, form):
        self.generate_document(str(self.kwargs["template_id"]))
        success_message = "Generated document successfully"
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        # TODO: Redirect the user to the landing screen when we have a document
        return reverse("cases:f680:document:all", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        template_id = str(self.kwargs["template_id"])
        preview_response, _ = self.get_generated_document_preview(template_id=template_id)
        context_data.update(
            {
                "preview": preview_response["preview"],
            }
        )
        return context_data
