from http import HTTPStatus

from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import FormView


from caseworker.advice.services import post_bulk_approval_recommendation
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class BulkApprovalForm(forms.Form):
    pass


class BulkApprovalView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Submit approval recommendation for the selected cases
    """

    template_name = "core/form.html"
    form_class = BulkApprovalForm

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

    def form_valid(self, form):
        queue_id = self.kwargs["pk"]
        cases = self.request.POST.getlist("cases", [])
        payload = {
            "cases": cases,
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

        num_cases = len(cases)
        success_message = f"Successfully approved {num_cases} cases"
        if num_cases == 1:
            success_message = "Successfully approved 1 case"
        messages.success(self.request, success_message)

        return super().form_valid(form)
