from exporter.f680.application_sections.views import F680MultipleItemApplicationSectionWizard

from .constants import FormSteps
from .forms import EntityTypeForm, EndUserNameForm, EndUserAddressForm, SecurityGradingForm, EndUserIntendedEndUseForm


class UserInformationView(F680MultipleItemApplicationSectionWizard):
    form_list = [
        (FormSteps.ENTITY_TYPE, EntityTypeForm),
        (FormSteps.END_USER_NAME, EndUserNameForm),
        (FormSteps.END_USER_ADDRESS, EndUserAddressForm),
        (FormSteps.SECURITY_GRADING, SecurityGradingForm),
        (FormSteps.INTENDED_END_USE, EndUserIntendedEndUseForm),
    ]
    section = "user_information"
    section_label = "User Information"
