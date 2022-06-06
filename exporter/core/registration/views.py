import logging
from http import HTTPStatus

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect

from lite_forms.generators import error_page
from core.auth.views import LoginRequiredMixin

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.applications.views.goods.add_good_firearm.views.decorators import expect_status
from exporter.applications.views.goods.add_good_firearm.views.exceptions import ServiceError
from exporter.auth.services import authenticate_exporter_user

from .constants import RegistrationSteps
from .forms import (
    RegistrationTypeForm,
    RegistrationUKBasedForm,
    RegisterIndividualDetailsForm,
    RegisterAddressDetailsForm,
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
        (RegistrationSteps.INDIVIDUAL_DETAILS, RegisterIndividualDetailsForm),
        (RegistrationSteps.ADDRESS_DETAILS, RegisterAddressDetailsForm),
    ]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == RegistrationSteps.ADDRESS_DETAILS:
            kwargs["is_uk_based"] = self.is_uk_based
        return kwargs

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
        try:
            self.post_registration(form_dict)
        except ServiceError as e:
            return self.handle_service_error(e)
        self.update_authenticate_exporter_user()
        return redirect(self.get_success_url())

    def update_authenticate_exporter_user(self):
        # Update the signed in user's details so they can make validated API calls
        response, _ = authenticate_exporter_user(
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

    def get_success_url(self):
        return reverse("core:register_an_organisation_confirm") + "?animate=True"

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise service_error
        return error_page(self.request, service_error.user_message)

    @property
    def is_uk_based(self):
        return self.get_cleaned_data_for_step(RegistrationSteps.UK_BASED)["location"] == "united_kingdom"
