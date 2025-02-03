from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

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

from django.core.exceptions import PermissionDenied


class F680FeatureDenied(PermissionDenied):
    pass


class F680FeatureRequiredMixin(AccessMixin):  # PS-IGNORE

    def handle_no_permission(self):
        if not settings.FEATURE_FLAG_ALLOW_F680:
            raise F680FeatureDenied("You are not authorised to use the F680 Security Clearance application feature")


class F680ApplicationCreateView(LoginRequiredMixin, BaseSessionWizardView, F680FeatureRequiredMixin):  # PS-IGNORE
    form_list = [
        (ApplicationFormSteps.APPLICATION_NAME, ApplicationNameForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

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


class F680ApplicationSummaryView(LoginRequiredMixin, FormView, F680FeatureRequiredMixin):  # PS-IGNORE
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"  # PS-IGNORE

    def setup(self, request, *args, **kwargs):
        self.handle_no_permission()
        super().setup(request, *args, **kwargs)
        self.application = get_f680_application(request, kwargs["pk"])  # PS-IGNORE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.application

        return context

    def get_success_url(self):
        return reverse("f680:summary", kwargs={"pk": self.application["id"]})  # PS-IGNORE
