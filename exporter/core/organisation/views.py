import requests
import logging
from http import HTTPStatus

from django.http import Http404
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.utils.functional import cached_property

from core.auth.views import LoginRequiredMixin
from core.auth.utils import get_profile
from core.decorators import expect_status


from exporter.core.wizard.views import BaseSessionWizardView
from exporter.auth.services import authenticate_exporter_user
from exporter.organisation.members.services import get_user
from exporter.core.services import get_organisation
from exporter.core.constants import OrganisationStatus

from .constants import RegistrationSteps
from .forms import (
    RegistrationTypeForm,
    RegistrationUKBasedForm,
    RegisterDetailsForm,
    RegisterAddressDetailsForm,
    SelectOrganisationForm,
    RegistrationEditName,
    RegistrationEditSICNumber,
    RegistrationEditEoriNumber,
    RegistrationEditVatNumber,
    RegistrationEditAddressName,
    RegistrationEditAddress,
    RegistrationEditAddress1,
    RegistrationEditAddress2,
    RegistrationEditCity,
    RegistrationEditRegion,
    RegistrationEditPostCode,
    RegistrationEditPhoneNumber,
    RegistrationEditWebsite,
    RegistrationEditCountry,
    RegistrationEditRegistrationNumber,
)
from .services import register_organisation, update_organisation
from .payloads import RegistrationPayloadBuilder

logger = logging.getLogger(__name__)


class OrganisationMixin:
    @cached_property
    def organisation(self):
        try:
            organisation = get_user(self.request, params={OrganisationStatus.DRAFT: True})["organisations"][0]
        except requests.exceptions.HTTPError:
            raise Http404("Couldn't get organisation")

        return get_organisation(self.request, organisation["id"])

    @cached_property
    def organisation_id(self):
        return self.organisation["id"]

    @cached_property
    def is_uk_based(self):
        return self.organisation["primary_site"]["address"]["country"]["id"] == "GB"


class Registration(
    BaseSessionWizardView,
    LoginRequiredMixin,
    OrganisationMixin,
):
    form_list = [
        (RegistrationSteps.REGISTRATION_TYPE, RegistrationTypeForm),
        (RegistrationSteps.UK_BASED, RegistrationUKBasedForm),
        (RegistrationSteps.REGISTRATION_DETAILS, RegisterDetailsForm),
        (RegistrationSteps.ADDRESS_DETAILS, RegisterAddressDetailsForm),
    ]

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == RegistrationSteps.ADDRESS_DETAILS:
            kwargs["is_uk_based"] = self.is_uk_based
        if step == RegistrationSteps.REGISTRATION_DETAILS:
            kwargs["is_individual"] = self.is_individual
        return kwargs

    @expect_status(
        HTTPStatus.CREATED,
        "Error registering user",
        "Unexpected error registering user",
    )
    def post_registration(self, form_dict):
        payload = RegistrationPayloadBuilder().build(form_dict)
        payload["status"] = OrganisationStatus.DRAFT
        return register_organisation(
            self.request,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        # We need to set the session for email for post
        # may be we do else where
        profile = get_profile(self.request.authbroker_client)
        self.request.session["email"] = profile["email"]
        new_org = self.post_registration(form_dict)
        self.update_authenticate_exporter_user(new_org)
        return redirect(self.get_success_url())

    @expect_status(
        HTTPStatus.OK,
        "Error updating registered user",
        "Unexpected updating registered user",
    )
    def update_authenticate_exporter_user(self, new_org):
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
        self.request.session["organisation"] = new_org[0]["id"]
        self.request.session["organisation_name"] = new_org[0]["name"]
        return response, status_code

    def get_success_url(self):
        return reverse("core:register_draft_confirm")

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
        return ctx


class DraftConfirmation(TemplateView, OrganisationMixin):
    template_name = "organisation/registration/draft-organisation-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "organisation": self.organisation,
                "is_uk_based": self.is_uk_based,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        update_organisation(request, self.organisation_id, {"status": OrganisationStatus.REVIEW})
        return redirect(reverse("core:register_an_organisation_confirm") + "?animate=True")


class BaseOrganisationEditView(
    LoginRequiredMixin,
    OrganisationMixin,
    FormView,
):
    template_name = "core/form.html"
    field_name = None
    form_class = None

    def get_success_url(self):
        return reverse("core:register_draft_confirm")

    def form_valid(self, form):
        if self.is_address_name:
            payload = {"site": form.cleaned_data}
            if self.organisation["primary_site"]["address"].get("address_line_1"):
                payload["site"].update(
                    {"address": {"address_line_1": self.organisation["primary_site"]["address"]["address_line_1"]}}
                )
            else:
                payload["site"].update({"address": self.organisation["primary_site"]["address"]})
        elif self.is_address_field:
            payload = {"site": {"address": form.cleaned_data}}
            # This is a hack for BE address serializer won't load GB country unless it sees address_line_1
            if self.is_uk_based and self.field_name != "address_line_1":
                payload["site"]["address"]["address_line_1"] = self.organisation["primary_site"]["address"][
                    "address_line_1"
                ]
            elif self.field_name == "address":
                payload["site"]["address"]["country"] = self.organisation["primary_site"]["address"]["country"]
        else:
            payload = form.cleaned_data
        update_organisation(self.request, self.organisation_id, payload)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["back_link_url"] = reverse("core:register_draft_confirm")
        return ctx

    @property
    def is_address_field(self):
        return self.field_name in self.address_fields


class OrganisationEditField(BaseOrganisationEditView):
    dict_forms = {
        "sic_number": RegistrationEditSICNumber,
        "name": RegistrationEditName,
        "eori_number": RegistrationEditEoriNumber,
        "vat_number": RegistrationEditVatNumber,
        "registration_number": RegistrationEditRegistrationNumber,
        "address_name": RegistrationEditAddressName,
        "address": RegistrationEditAddress,
        "address_line_1": RegistrationEditAddress1,
        "address_line_2": RegistrationEditAddress2,
        "city": RegistrationEditCity,
        "region": RegistrationEditRegion,
        "postcode": RegistrationEditPostCode,
        "phone_number": RegistrationEditPhoneNumber,
        "website": RegistrationEditWebsite,
        "country": RegistrationEditCountry,
    }

    address_fields = [
        "address_name",
        "address",
        "address_line_1",
        "address_line_2",
        "city",
        "region",
        "postcode",
        "country",
    ]
    is_address_name = False

    def dispatch(self, request, *args, **kwargs):
        if kwargs["field"] == "address_name":
            # Let's make a special case for address_name since name clashes with name field
            self.form_class = self.dict_forms["address_name"]
            self.field_name = "name"
            self.is_address_name = True
        else:
            self.field_name = kwargs["field"]
            self.form_class = self.dict_forms[self.field_name]

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        if self.is_address_name:
            field_value = self.organisation["primary_site"][self.field_name]
        elif self.is_address_field:
            field_value = self.organisation["primary_site"]["address"][self.field_name]
        else:
            field_value = self.organisation[self.field_name]
        return {self.field_name: field_value}
