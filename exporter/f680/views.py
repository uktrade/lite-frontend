from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.f680.constants import ApplicationFormSteps
from exporter.f680.forms import (
    ApplicationNameForm,
    ApplicationSubmissionForm,
)
from exporter.f680.payloads import F680CreatePayloadBuilder
from exporter.f680.services import (
    get_680_application,
    post_f680_application,
)


class F680ApplicationCreateView(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (ApplicationFormSteps.APPLICATION_NAME, ApplicationNameForm),
    ]

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",
        "Unexpected Error creating F680 application",
    )
    def post_f680_application(self, data):
        return post_f680_application(self.request, data)

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",
            kwargs={
                "pk": application_id,
            },
        )

    def get_payload(self, form_dict):
        return F680CreatePayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.post_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationSummaryView(LoginRequiredMixin, FormView):
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["application"] = get_680_application(self.request, self.kwargs["pk"])["application"]

        return ctx
