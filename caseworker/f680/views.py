from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View
import rules

from core.auth.views import LoginRequiredMixin

from caseworker.core.constants import ALL_CASES_QUEUE_ID
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
        if not rules.test_rule("can_user_move_case_forward", self.request, case):
            raise PermissionDenied("Cannot move case forward")

        move_case_forward(request, case_pk, queue_pk)

        all_cases_queue_url = reverse("cases:f680:details", kwargs={"queue_pk": ALL_CASES_QUEUE_ID, "pk": case_pk})
        # WARNING: When changing this message be aware that the content is marked
        #   as safe. No user-supplied string should be injected in to it
        success_message = mark_safe(  # noqa: S308
            f"<a href='{all_cases_queue_url}' class='govuk-link govuk-link--inverse'>{case.reference_code}</a>&nbsp;"
            "was successfully moved forward"
        )
        messages.success(self.request, success_message, extra_tags="safe")
        queue_url = reverse("queues:cases", kwargs={"queue_pk": queue_pk})
        return redirect(queue_url)
