from http import HTTPStatus
from django.views.generic import TemplateView

from caseworker.cases.helpers.helpers import generate_document_error_page
from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import (
    get_case,
    get_f680_final_decision_documents,
    get_generated_document_preview,
    post_generated_document,
)
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.queues.services import get_queue
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class CaseDetailView(LoginRequiredMixin, CaseworkerMixin, TemplateView):
    template_name = "f680/case/detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        return context_data


class F680DocumentsView(LoginRequiredMixin, CaseworkerMixin, TemplateView):
    template_name = "f680/case/f680-final-advice-documents.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        document, _ = get_f680_final_decision_documents(self.request, self.case_id)
        context_data["document"] = document["document"]
        return context_data


class F680PreviewDocument(LoginRequiredMixin, CaseworkerMixin, TemplateView):
    def get(self, request, **kwargs):
        template_id = "ab19ef84-48e8-4677-b8dd-7ae64d18a137"
        case_id = str(kwargs["pk"])
        preview, status_code = get_generated_document_preview(
            request, case_id, template=template_id, text=None, addressee=None
        )
        if status_code == 400:
            return generate_document_error_page()

        return render(
            self.request,
            "f680/case/f680-preview.html",
            {"preview": preview["preview"], "text": "", "addressee": "", "kwargs": self.kwargs},
        )


class F680CreateDocument(LoginRequiredMixin, CaseworkerMixin, TemplateView):
    def post(
        self,
        request,
        queue_pk,
        pk,
    ):
        template_id = "ab19ef84-48e8-4677-b8dd-7ae64d18a137"
        status_code = post_generated_document(
            request,
            str(pk),
            {"template": template_id, "text": "", "addressee": "", "visible_to_exporter": True},
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(
                reverse_lazy("cases:f680:generate_document_view", kwargs={"queue_pk": queue_pk, "pk": str(pk)})
            )
