from http import HTTPStatus

from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from conf import base as settings
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from .constants import (
    ApplicationFormSteps,
)
from .forms import (
    ApplicationNameForm,
    ApplicationSubmissionForm,
)
from .payloads import (
    F680CreatePayloadBuilder,  # PS-IGNORE
)
from .services import (
    post_f680_application,  # PS-IGNORE
    get_f680_application,
)


class F680FeatureRequiredMixin(AccessMixin):  # PS-IGNORE
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_ALLOW_F680:  # PS-IGNORE
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_permission_denied_message(self):
        self.permission_denied_message = "You are not authorised to use this feature"
        return self.permission_denied_message


class F680ApplicationCreateView(LoginRequiredMixin, BaseSessionWizardView):  # PS-IGNORE
    form_list = [
        (ApplicationFormSteps.APPLICATION_NAME, ApplicationNameForm),
    ]

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",  # PS-IGNORE
        "Unexpected error creating F680 application",
    )
    def post_f680_application(self, data):  # PS-IGNORE
        return post_f680_application(self.request, data)  # PS-IGNORE

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",  # PS-IGNORE
            kwargs={
                "pk": application_id,
            },
        )

    def get_payload(self, form_dict):
        return F680CreatePayloadBuilder().build(form_dict)  # /PS-IGNORE

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.post_f680_application(data)  # PS-IGNORE
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationSummaryView(LoginRequiredMixin, FormView):  # PS-IGNORE
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"  # PS-IGNORE

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.application = get_f680_application(request, kwargs["pk"])  # PS-IGNORE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.application

        return context

    def get_success_url(self):
        return reverse("f680:summary", kwargs={"pk": self.application["id"]})  # PS-IGNORE
