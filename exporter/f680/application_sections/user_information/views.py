from exporter.f680.application_sections.views import F680MultipleItemApplicationSectionWizard

from .constants import FormSteps
from .forms import EntityTypeForm


class UserInformationView(F680MultipleItemApplicationSectionWizard):
    form_list = [
        (FormSteps.ENTITY_TYPE, EntityTypeForm),
    ]
    section = "user_information"
    section_label = "User Information"
