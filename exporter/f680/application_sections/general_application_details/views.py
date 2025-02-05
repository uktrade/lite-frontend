from http import HTTPStatus
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.f680.services import patch_f680_application, get_f680_application
from exporter.f680.payloads import F680PatchPayloadBuilder
from exporter.f680.views import F680FeatureRequiredMixin

from .constants import FormSteps
from .forms import ApplicationNameForm, ExceptionalCircumstancesForm, ExplainExceptionalCircumstancesForm


class GeneralApplicationDetailsView(LoginRequiredMixin, F680FeatureRequiredMixin, BaseSessionWizardView):
    form_list = [
        (FormSteps.APPLICATION_NAME, ApplicationNameForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES, ExceptionalCircumstancesForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS, ExplainExceptionalCircumstancesForm),
    ]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application = get_f680_application(request, kwargs["pk"])

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def patch_f680_application(self, data):
        return patch_f680_application(self.request, self.application["id"], data)

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",
            kwargs={
                "pk": application_id,
            },
        )

    def get_payload(self, form_dict):
        section = "general_application_details"
        current_application = self.application["application"]
        return F680PatchPayloadBuilder().build(section, current_application, form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.patch_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))
