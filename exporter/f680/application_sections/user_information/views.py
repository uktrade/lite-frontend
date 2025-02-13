from exporter.core.services import get_countries
from exporter.f680.application_sections.views import F680MultipleItemApplicationSectionWizard

from .constants import FormSteps
from .forms import (
    EntityTypeForm,
    ThirdPartyRoleForm,
    EndUserNameForm,
    EndUserAddressForm,
    SecurityGradingForm,
    EndUserIntendedEndUseForm,
    EndUserAssembleManufactureForm,
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
        (FormSteps.ASSEMBLE_MANUFACTURE, EndUserAssembleManufactureForm),
    ]
    condition_dict = {
        FormSteps.THIRD_PARTY_ROLE: is_third_party,
    }
    section = "user_information"
    section_label = "User Information"

    def get_form_kwargs(self, step):
        if step == FormSteps.END_USER_ADDRESS:
            countries = get_countries(self.request, False, ["GB"])
            return {"countries": countries}
        return {}
