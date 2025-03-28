from http import HTTPStatus
import rules

from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView


from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from .forms import ApplicationSubmissionForm

from .services import (
    get_f680_application,
    submit_f680_application,
)

from exporter.applications.services import (
    get_activity,
    get_application_history,
    get_case_notes,
    get_case_generated_documents,
    get_application_ecju_queries,
    get_application,
    post_case_notes,
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


class F680ApplicationSummaryView(LoginRequiredMixin, F680FeatureRequiredMixin, FormView):
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])

    @expect_status(
        HTTPStatus.OK,
        "Error getting F680 application",
        "Unexpected error getting F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, application_id):
        return get_f680_application(self.request, application_id)

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

    def all_sections_complete(self):
        # TODO: Think more about pre-submit validation as this is very barebones right now
        complete_sections = set(self.application["application"].get("sections", {}).keys())
        required_sections = set(
            [
                "general_application_details",
                "approval_type",
                "user_information",
                "product_information",
            ]
        )
        missing_sections = required_sections - complete_sections
        return len(missing_sections) == 0, missing_sections

    def form_valid(self, form):
        is_sections_completed, _ = self.all_sections_complete()
        if not is_sections_completed:
            context_data = self.get_context_data(form=form)
            context_data["errors"] = {"missing_sections": ["Please complete all required sections"]}
            return self.render_to_response(context_data)

        self.submit_f680_application(self.application["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:success_page", kwargs={"pk": self.application["id"]})


class F680ApplicationDetailView(LoginRequiredMixin, F680FeatureRequiredMixin, TemplateView):
    template_name = "f680/application_detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application = get_application(request, str(kwargs["pk"]))
        self.get_application_history = get_application_history(self.request, str(kwargs["pk"]))
        self.view_type = kwargs.get("type", None)

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.application
        context["application_history"] = self.get_application_history
        application_section_order = [
            "general_application_details",
            "approval_type",
            "product_information",
            "user_information",
            "supporting_documents",
            "notes_for_case_officers",
        ]
        application_sections = {
            key: self.application["application"]["sections"].get(key, None) for key in application_section_order
        }

        context["application_sections"] = application_sections
        context["activity"] = (get_activity(self.request, self.application["id"]) or {},)
        if self.view_type == "case-notes":
            context["notes"] = get_case_notes(self.request, self.application["id"])["case_notes"]

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(
                self.request, self.application["id"]
            )
        if self.view_type == "generated-documents":
            generated_documents, _ = get_case_generated_documents(self.request, self.application["id"])
            context["generated_documents"] = generated_documents["results"]
        return context

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            raise Http404()
        response, _ = post_case_notes(request, self.application["id"], request.POST)
        if "errors" in response:
            return self.get(request, error=response["errors"], text=request.POST.get("text"), **kwargs)
        return redirect(reverse("f680:detail", kwargs={"pk": self.application["id"], "type": "case-notes"}))
