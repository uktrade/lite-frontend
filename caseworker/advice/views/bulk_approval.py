import rules

from http import HTTPStatus

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import View


from caseworker.advice.services import post_bulk_approval_recommendation
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class BulkApprovalView(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    Submit approval recommendation for the selected cases
    """

    def dispatch(self, *args, **kwargs):

        if not rules.test_rule("can_user_bulk_approve_cases", self.request, self.kwargs["pk"]):
            raise Http404()
        return super().dispatch(*args, **kwargs)

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    def get_success_url(self):
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})

    @expect_status(
        HTTPStatus.CREATED,
        "Error submitting bulk approval recommendation",
        "Unexpected error submitting bulk approval recommendation",
    )
    def submit_bulk_approval_recommendation(self, queue_id, payload):
        return post_bulk_approval_recommendation(self.request, queue_id, payload)

    def post(self, request, *args, **kwargs):
        queue_id = self.kwargs["pk"]
        cases = self.request.POST.getlist("cases", [])
        payload = {
            "cases": cases,
            "advice": {
                "text": "No concerns: Approved using bulk approval",
                "proviso": "",
                "note": "",
                "footnote_required": False,
                "footnote": "",
                "team": str(self.caseworker["team"]["id"]),
            },
        }

        self.submit_bulk_approval_recommendation(queue_id, payload)

        num_cases = len(cases)
        success_message = f"Successfully approved {num_cases} cases"
        if num_cases == 1:
            success_message = "Successfully approved 1 case"
        messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())
