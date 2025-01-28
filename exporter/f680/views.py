from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.applications.services import submit_application

from exporter.f680.constants import ApplicationFormSteps, ProductFormSteps, EndUserFormSteps
from exporter.f680.forms import (
    ApplicationNameForm,
    ApplicationPreviousApplicationForm,
    ApplicationSubmissionForm,
    ProductNameAndDescriptionForm,
    EndUserNameForm,
)
from exporter.f680.payloads import (
    F680CreatePayloadBuilder,
    F680CreateProductPayloadBuilder,
    F680CreateEndUserPayloadBuilder,
)
from exporter.f680.services import (
    get_f680_application,
    post_f680_application,
)


class F680ApplicationCreateView(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (ApplicationFormSteps.APPLICATION_NAME, ApplicationNameForm),
        (ApplicationFormSteps.PREVIOUS_APPLICATION, ApplicationPreviousApplicationForm),
    ]

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

    def get_payload(self, form_dict):
        return F680CreatePayloadBuilder(self).build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.post_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationSummaryView(LoginRequiredMixin, FormView):
    form_class = ApplicationSubmissionForm
    template_name = "f680/summary.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.application = get_f680_application(request, kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["application"] = self.application

        return ctx

    @expect_status(
        HTTPStatus.OK,
        "Error submitting F680 application",
        "Unexpected error submitting F680 application",
    )
    def submit_application(self, request, application_id):
        return submit_application(
            request,
            application_id,
            {"submit_declaration": True, "agreed_to_foi": False, "agreed_to_declaration_text": "i agree"},
        )

    def form_valid(self, form):
        self.submit_application(self.request, self.application["id"])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("f680:submitted", kwargs={"pk": self.application["id"]})


class F680ApplicationSubmittedView(TemplateView):
    template_name = "f680/submitted.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.application = get_f680_application(request, kwargs["pk"])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["application"] = self.application["application"]
        context_data["reference_code"] = self.application["reference_code"]

        return context_data


class F680ApplicationProductsView(LoginRequiredMixin, BaseSessionWizardView):  # PS-IGNORE
    form_list = [
        (ProductFormSteps.NAME_AND_DESCRIPTION, ProductNameAndDescriptionForm),
    ]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.application = get_f680_application(request, kwargs["pk"])  # PS-IGNORE

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",  # PS-IGNORE
        "Unexpected error creating F680 application",  # PS-IGNORE
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
        return F680CreateProductPayloadBuilder(self).build(  # PS-IGNORE
            form_dict,
            {
                "application": {
                    **self.application["application"],
                    "products": self.application["application"].get("products", []),
                },
            },
        )

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.post_f680_application(data)  # PS-IGNORE
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationPartyView(LoginRequiredMixin, BaseSessionWizardView):  # PS-IGNORE

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.application = get_f680_application(request, kwargs["pk"])  # PS-IGNORE

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",  # PS-IGNORE
        "Unexpected error creating F680 application",  # PS-IGNORE
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

    def get_payload(self, form_dict, party_type, payload_builder_class):
        return payload_builder_class(self).build(
            form_dict,
            {
                "application": {
                    **self.application["application"],
                    party_type: self.application["application"].get(party_type, []),
                },
            },
        )

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict, self.party_type, self.payload_builder_class)
        response_data, _ = self.post_f680_application(data)  # PS-IGNORE
        return redirect(self.get_success_url(response_data["id"]))


class F680ApplicationEndUserView(F680ApplicationPartyView):  # PS-IGNORE
    form_list = [
        (EndUserFormSteps.END_USER_NAME, EndUserNameForm),
    ]

    payload_builder_class = F680CreateEndUserPayloadBuilder  # PS-IGNORE
