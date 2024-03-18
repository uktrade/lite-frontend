import logging
from http import HTTPStatus

from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from core.wizard.views import BaseSessionWizardView
from exporter.auth.services import authenticate_exporter_user
from exporter.organisation.members.services import get_user
from exporter.core.services import get_organisation

from .constants import RegistrationSteps
from .forms import (
    RegistrationTypeForm,
    RegistrationUKBasedForm,
    RegisterDetailsIndividualUKForm,
    RegisterDetailsIndividualOverseasForm,
    RegisterDetailsCommercialUKForm,
    RegisterDetailsCommercialOverseasForm,
    RegisterAddressDetailsUKForm,
    RegisterAddressDetailsOverseasForm,
    SelectOrganisationForm,
)
from .services import register_organisation
from .payloads import RegistrationPayloadBuilder

logger = logging.getLogger(__name__)


class Registration(
    BaseSessionWizardView,
    LoginRequiredMixin,
):
    form_list = [
        (RegistrationSteps.REGISTRATION_TYPE, RegistrationTypeForm),
        (RegistrationSteps.UK_BASED, RegistrationUKBasedForm),
        (RegistrationSteps.REGISTRATION_DETAILS, RegisterDetailsIndividualUKForm),
        (RegistrationSteps.ADDRESS_DETAILS, RegisterAddressDetailsUKForm),
    ]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step in (RegistrationSteps.ADDRESS_DETAILS):
            kwargs["is_individual"] = self.is_individual
        return kwargs

    def get_form(self, step=None, data=None, files=None):
        # form = super().get_form(step, data, files)
        # determine the step if not given
        form = super().get_form(step, data, files)
        if step is None:
            step = self.steps.current

        if step == RegistrationSteps.REGISTRATION_DETAILS:
            form = self.get_registration_details_form(data)

        if step == RegistrationSteps.ADDRESS_DETAILS:
            form = self.get_registration_address_form(data)

        return form

    def get_registration_details_form(self, data):
        location = self.get_cleaned_data_for_step(RegistrationSteps.UK_BASED)["location"]
        registration_type = self.get_cleaned_data_for_step(RegistrationSteps.REGISTRATION_TYPE)["type"]
        registration_details_form_classes = {
            "united_kingdom": {
                "individual": RegisterDetailsIndividualUKForm,
                "commercial": RegisterDetailsCommercialUKForm,
            },
            "abroad": {
                "individual": RegisterDetailsIndividualOverseasForm,
                "commercial": RegisterDetailsCommercialOverseasForm,
            },
        }
        form_class = registration_details_form_classes[location][registration_type]
        kwargs = {
            "prefix": self.get_form_prefix(RegistrationSteps.REGISTRATION_DETAILS, form_class),
            "data": data,
        }
        return form_class(**kwargs)

    def get_registration_address_form(self, data):
        location = self.get_cleaned_data_for_step(RegistrationSteps.UK_BASED)["location"]
        form_class = (
            RegisterAddressDetailsUKForm if location == "united_kingdom" else RegisterAddressDetailsOverseasForm
        )
        kwargs = self.get_form_kwargs(RegistrationSteps.ADDRESS_DETAILS)
        kwargs.update(
            {
                "prefix": self.get_form_prefix(RegistrationSteps.ADDRESS_DETAILS, form_class),
                "data": data,
            }
        )
        return form_class(**kwargs)

    @expect_status(
        HTTPStatus.CREATED,
        "Error registering user",
        "Unexpected error registering user",
    )
    def post_registration(self, form_dict):
        payload = RegistrationPayloadBuilder().build(form_dict)
        return register_organisation(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.post_registration(form_dict)
        self.update_authenticate_exporter_user()
        return redirect(self.get_success_url())

    @expect_status(
        HTTPStatus.OK,
        "Error updating registered user",
        "Unexpected updating registered user",
    )
    def update_authenticate_exporter_user(self):
        # Update the signed in user's details so they can make validated API calls
        response, status_code = authenticate_exporter_user(
            self.request,
            {
                "email": self.request.session["email"],
                "user_profile": {
                    "first_name": self.request.session["first_name"],
                    "last_name": self.request.session["last_name"],
                },
            },
        )

        self.request.session["user_token"] = response["token"]
        self.request.session["lite_api_user_id"] = response["lite_api_user_id"]
        return response, status_code

    def get_success_url(self):
        return reverse("core:register_an_organisation_confirm") + "?animate=True"

    @property
    def is_uk_based(self):
        return self.get_cleaned_data_for_step(RegistrationSteps.UK_BASED)["location"] == "united_kingdom"

    @property
    def is_individual(self):
        return self.get_cleaned_data_for_step(RegistrationSteps.REGISTRATION_TYPE)["type"] == "individual"


class SelectOrganisation(LoginRequiredMixin, FormView):
    form_class = SelectOrganisationForm
    template_name = "core/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = get_user(self.request)
        kwargs["organisations"] = user["organisations"]
        return kwargs

    def form_valid(self, form):
        organisation_id = form.cleaned_data["organisation"]

        self.request.session["organisation"] = organisation_id
        organisation = get_organisation(self.request, organisation_id)

        if "errors" in organisation:
            return redirect(reverse("core:register_an_organisation_confirm") + "?show_back_link=True")

        self.request.session["organisation_name"] = organisation["name"]

        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.GET.get("back_link") == "applications":
            success_url = reverse("applications:applications")
            if self.request.GET.get("submitted"):
                success_url = success_url + "?submitted=False"
        elif self.request.GET.get("back_link") == "licences":
            success_url = reverse("licences:list-open-and-standard-licences")
        else:
            success_url = reverse("core:home")
        return success_url

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.GET.get("back_link") == "applications":
            ctx["back_link_text"] = "Back to applications"
        elif self.request.GET.get("back_link") == "licences":
            ctx["back_link_text"] = "Back to licences"
        ctx["back_link_url"] = self.get_success_url()
        ctx["form_title"] = SelectOrganisationForm.Layout.TITLE
        return ctx
