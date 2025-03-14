from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import (
    ApplicationNameForm,
    PreviousApplicationConfirm,
    PreviousApplicationsForm,
    ExceptionalCircumstancesForm,
    ExplainExceptionalCircumstancesForm,
)


def is_exceptional_circumstances(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.EXCEPTIONAL_CIRCUMSTANCES) or {}
    return cleaned_data.get("is_exceptional_circumstances", False)


def has_made_previous_application(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.HAS_MADE_PREVIOUS_APPLICATION) or {}
    return cleaned_data.get("has_made_previous_application", False)


class GeneralApplicationDetailsView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.APPLICATION_NAME, ApplicationNameForm),
        (FormSteps.HAS_MADE_PREVIOUS_APPLICATION, PreviousApplicationConfirm),
        (FormSteps.PREVIOUS_APPLICATION, PreviousApplicationsForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES, ExceptionalCircumstancesForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS, ExplainExceptionalCircumstancesForm),
    ]
    condition_dict = {
        FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS: is_exceptional_circumstances,
        FormSteps.PREVIOUS_APPLICATION: has_made_previous_application,
    }
    section = "general_application_details"
    section_label = "General application details"
