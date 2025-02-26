from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import get_case
from caseworker.advice.services import move_case_forward
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.queues.services import get_queue


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
        submitted_by = self.case["data"]["submitted_by"]
        if submitted_by and "first_name" in submitted_by:
            self.case["data"]["submitted_by"] = " ".join([submitted_by["first_name"], submitted_by["last_name"]])
        context_data["case"] = self.case
        return context_data


class MoveCaseForward(LoginRequiredMixin, View):

    def post(self, request, queue_pk, pk):
        queue_pk = str(queue_pk)
        case_pk = str(pk)
        case = get_case(request, case_pk)
        move_case_forward(request, case_pk, queue_pk)
        messages.success(self.request, f"{case.reference_code} was successfully moved forward")
        queue_url = reverse("queues:cases", kwargs={"queue_pk": queue_pk})
        return redirect(queue_url)
