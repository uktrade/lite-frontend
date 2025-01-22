from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.f680.constants import ApplicationFormSteps
from exporter.f680.forms import ApplicationNameForm
from exporter.f680.payloads import F680CreatePayloadBuilder
from exporter.f680.services import post_f680_application


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


class F680ApplicationSummaryView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")
