from http import HTTPStatus
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.core.constants import AddF680FormSteps  # /PS-IGNORE
from exporter.applications.constants import ApplicationStatus
from exporter.applications.helpers.task_lists import get_application_task_list
from exporter.applications.services import post_f680_application, get_f680_application

from .forms import f680InitialForm, F680NameForm  # /PS-IGNORE
from .payloads import AddF680PayloadBuilder  # /PS-IGNORE


class AddF680(LoginRequiredMixin, BaseSessionWizardView):  # /PS-IGNORE
    form_list = [
        (AddF680FormSteps.F680_NAME, F680NameForm),  # /PS-IGNORE
        (AddF680FormSteps.F680INITIAL, f680InitialForm),  # /PS-IGNORE
    ]

    def get_form_kwargs(self, step=None):
        return super().get_form_kwargs(step)

    def get_payload(self, form_dict):
        return AddF680PayloadBuilder().build(form_dict)  # /PS-IGNORE

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding F680 application",
        "Unexpected error adding adding F680 application",
    )
    def post_application_with_payload(self, form_dict):
        payload = self.get_payload(form_dict)
        payload.update({"application_type": "f680"})  # /PS-IGNORE
        return post_f680_application(self.request, payload)

    def done(self, form_list, form_dict, **kwargs):
        response, _ = self.post_application_with_payload(form_dict)
        return redirect(reverse_lazy("f680:f680_task_list", kwargs={"pk": response["id"]}))


class GetF680Application(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application = get_f680_application(request, kwargs["pk"])
        if application["status"]["key"] not in [ApplicationStatus.DRAFT, ApplicationStatus.APPLICANT_EDITING]:
            return redirect(reverse("applications:application", kwargs={"pk": kwargs["pk"]}))
        return get_application_task_list(request, application)
