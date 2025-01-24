from http import HTTPStatus
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.core.constants import AddF680FormSteps  # /PS-IGNORE
from exporter.applications.constants import ApplicationStatus
from exporter.applications.helpers.task_lists import get_application_task_list
from exporter.applications.services import post_f680_application, put_f680_application, get_f680_application

from .forms import f680InitialForm, F680NameForm  # /PS-IGNORE
from .payloads import AddF680PayloadBuilder  # /PS-IGNORE


class F680Create(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = F680NameForm

    def form_valid(self, form):
        self.name = form.cleaned_data["name"]
        return super().form_valid(form)

    def get_success_url(self):
        data = {"name": self.name, "data": {}}
        response, _ = post_f680_application(self.request, data)
        return reverse_lazy("f680:f680_task_list", kwargs={"pk": response["id"]})


class GetF680Application(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application = get_f680_application(request, kwargs["pk"])

        if application["status"]["key"] not in [ApplicationStatus.DRAFT, ApplicationStatus.APPLICANT_EDITING]:
            return redirect(reverse("applications:application", kwargs={"pk": kwargs["pk"]}))
        return get_application_task_list(request, application)


class F680ApprovalQuestions(LoginRequiredMixin, BaseSessionWizardView):  # /PS-IGNORE
    form_list = [
        (AddF680FormSteps.F680INITIAL, f680InitialForm),  # /PS-IGNORE
    ]

    def get_form_kwargs(self, step=None):
        return super().get_form_kwargs(step)

    def get_payload(self, form_dict):
        return AddF680PayloadBuilder().build(form_dict)  # /PS-IGNORE

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def update_application_with_payload(self, form_dict):
        payload = self.get_payload(form_dict)
        return put_f680_application(self.request, self.kwargs["pk"], payload)

    def done(self, form_list, form_dict, **kwargs):
        response, _ = self.update_application_with_payload(form_dict)
        return redirect(reverse_lazy("f680:f680_task_list", kwargs={"pk": response["pk"]}))
