from http import HTTPStatus

from django.views.generic import FormView
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from caseworker.f680.document.forms import DocumentGenerationForm
from caseworker.letter_templates.services import get_letter_templates_list

from caseworker.cases.services import get_case


class DocumentGenerationView(LoginRequiredMixin, FormView):
    form_class = DocumentGenerationForm
    template_name = "core/form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        # We will pull the decision from the case when filtering
        filter = {"case_type": self.case.case_type["sub_type"]["key"], "decision": "approve"}
        self.letter_templates, _ = self.get_letter_templates_list(filter)

    @expect_status(
        HTTPStatus.OK,
        "Error getting letter templates",
        "Unexpected error letter templates",
    )
    def get_letter_templates_list(self, filter):
        return get_letter_templates_list(self.request, filter)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["approval_template"] = self.letter_templates["results"]
        return form_kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        context_data["back_link_url"] = self.get_success_url()
        return context_data

    def get_success_url(self):
        return reverse("cases:f680:details", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})
