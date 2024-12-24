from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


from caseworker.advice.services import post_bulk_approval_recommendation
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class BulkApprovalView(LoginRequiredMixin, TemplateView):
    """
    Submit approval recommendation for the selected cases
    """

    template_name = "core/form.html"

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    @expect_status(
        HTTPStatus.CREATED,
        "Error submitting bulk approval recommendation",
        "Unexpected error submitting bulk approval recommendation",
    )
    def submit_bulk_approval_recommendation(self, queue_id, payload):
        return post_bulk_approval_recommendation(self.request, queue_id, payload)

    def post(self, request, *args, **kwargs):
        queue_id = self.kwargs["pk"]
        case_ids = self.request.GET.getlist("cases", [])
        payload = {
            "case_ids": case_ids,
            "advice": {
                "text": "Approved using bulk approval",
                "proviso": "",
                "note": "",
                "footnote_required": False,
                "footnote": "",
                "team": str(self.caseworker["team"]["id"]),
            },
        }

        self.submit_bulk_approval_recommendation(queue_id, payload)

        return redirect(reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]}))
