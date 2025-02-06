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


def is_exceptional_circumstances(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.EXCEPTIONAL_CIRCUMSTANCES) or {}
    return cleaned_data.get("is_exceptional_circumstances", False)


class GeneralApplicationDetailsView(LoginRequiredMixin, F680FeatureRequiredMixin, BaseSessionWizardView):
    form_list = [
        (FormSteps.APPLICATION_NAME, ApplicationNameForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES, ExceptionalCircumstancesForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS, ExplainExceptionalCircumstancesForm),
    ]
    condition_dict = {
        FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS: is_exceptional_circumstances,
    }
    section = "general_application_details"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving F680 application",
        "Unexpected error retrieving F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, pk):
        return get_f680_application(self.request, pk)

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def patch_f680_application(self, data):
        return patch_f680_application(self.request, self.application["id"], data)

    def get_form_initial(self, step):
        return self.application.get("application", {}).get(self.section, {}).get("answers", {})

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",
            kwargs={
                "pk": application_id,
            },
        )

    def get_payload(self, form_dict):
        current_application = self.application.get("application", {})
        return F680PatchPayloadBuilder().build(self.section, current_application, form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.patch_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))
