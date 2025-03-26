from http import HTTPStatus

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse

from core.decorators import expect_status

from exporter.core.services import get_countries
from exporter.f680.views import F680FeatureRequiredMixin
from exporter.f680.services import get_f680_application, patch_f680_application

from exporter.f680.application_sections.views import F680MultipleItemApplicationSectionWizard


from .constants import FormSteps
from .forms import (
    EntityTypeForm,
    ThirdPartyRoleForm,
    EndUserNameForm,
    EndUserAddressForm,
    SecurityGradingForm,
    EndUserIntendedEndUseForm,
)


def is_third_party(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.ENTITY_TYPE) or {}
    return cleaned_data.get("entity_type") == "third-party"


class UserInformationView(F680MultipleItemApplicationSectionWizard):
    form_list = [
        (FormSteps.ENTITY_TYPE, EntityTypeForm),
        (FormSteps.THIRD_PARTY_ROLE, ThirdPartyRoleForm),
        (FormSteps.END_USER_NAME, EndUserNameForm),
        (FormSteps.END_USER_ADDRESS, EndUserAddressForm),
        (FormSteps.SECURITY_GRADING, SecurityGradingForm),
        (FormSteps.INTENDED_END_USE, EndUserIntendedEndUseForm),
    ]
    condition_dict = {
        FormSteps.THIRD_PARTY_ROLE: is_third_party,
    }
    section = "user_information"
    section_label = "User Information"

    def get_form_kwargs(self, step, *args, **kwargs):
        if step == FormSteps.END_USER_ADDRESS:
            countries = get_countries(self.request, False, ["GB"])
            return {"countries": countries}
        return {}

    def get_success_url(self, application_id):
        return reverse(
            "f680:user_information:summary",
            kwargs={
                "pk": application_id,
            },
        )


class UserInformationSummaryView(F680FeatureRequiredMixin, TemplateView):
    template_name = "f680/user_information/summary.html"

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
        self.user_entities = self.get_user_entities()

    def get(self, request, *args, **kwargs):
        if not self.user_entities:
            return redirect(
                reverse(
                    "f680:user_information:wizard",
                    kwargs={
                        "pk": self.application["id"],
                    },
                )
            )
        return super().get(request, *args, **kwargs)

    def get_user_entities(self):
        if not self.application.get("application", {}).get("sections", {}).get("user_information", {}).get("items"):
            return {}
        user_entities = {}
        for entity in self.application["application"]["sections"]["user_information"]["items"]:
            answers = {field["key"]: field["answer"] for field in entity["fields"].values()}
            user_entities[entity["id"]] = answers
        return user_entities

    def get_context_data(self, pk, **kwargs):
        return {
            "application": self.application,
            "user_entities": self.user_entities,
        }


class UserInformationRemoveEntityView(F680FeatureRequiredMixin, TemplateView):

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

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def patch_f680_application(self, data):
        return patch_f680_application(self.request, self.application["id"], data)

    def remove_application_entity(self, entity_to_remove_id):
        application_data = self.application
        user_information_items = (
            application_data["application"].get("sections", {}).get("user_information", {}).get("items", [])
        )
        for item in user_information_items:
            if item["id"] == entity_to_remove_id:
                user_information_items.remove(item)
                self.patch_f680_application(application_data)

    def has_user_entities_remaining(self):
        application, _ = self.get_f680_application(self.application["id"])
        return application.get("application", {}).get("sections", {}).get("user_information", {}).get("items", [])

    def get(self, request, *args, **kwargs):
        self.remove_application_entity(kwargs["entity_to_remove_id"])
        if self.has_user_entities_remaining():
            return redirect(
                reverse(
                    "f680:user_information:summary",
                    kwargs={
                        "pk": self.application["id"],
                    },
                )
            )
        return redirect(reverse("f680:summary", kwargs={"pk": self.application["id"]}))
