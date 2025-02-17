from http import HTTPStatus
import rules

from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, RedirectView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from .forms import ApplicationSubmissionForm

from .services import (
    post_f680_application,
    get_f680_application,
    submit_f680_application,
)


class F680FeatureRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not rules.test_rule("can_exporter_use_f680s", request):
            self.raise_exception = True
            self.permission_denied_message = (
                "You are not authorised to use the F680 Security Clearance application feature"
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class F680ApplicationCreateView(LoginRequiredMixin, F680FeatureRequiredMixin, RedirectView):

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",
        "Unexpected error creating F680 application",
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

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # Data required to create a base application
        data = {"application": {}}
        response_data, _ = self.post_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationSummaryView(LoginRequiredMixin, F680FeatureRequiredMixin, FormView):
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"

    @expect_status(
        HTTPStatus.OK,
        "Error getting F680 application",
        "Unexpected error getting F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, application_id):
        return get_f680_application(self.request, application_id)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.application
        return context

    @expect_status(
        HTTPStatus.OK,
        "Error submitting F680 application",
        "Unexpected error submitting F680 application",
        reraise_404=True,
    )
    def submit_f680_application(self, application_id):
        return submit_f680_application(self.request, application_id)

    def form_valid(self, form):
        # TODO: Validate application payload before allowing submit
        self.submit_f680_application(self.application["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:home")
