from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import ApplicationNameForm, ExceptionalCircumstancesForm, ExplainExceptionalCircumstancesForm


def is_exceptional_circumstances(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.EXCEPTIONAL_CIRCUMSTANCES) or {}
    return cleaned_data.get("is_exceptional_circumstances", False)


class GeneralApplicationDetailsView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.APPLICATION_NAME, ApplicationNameForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES, ExceptionalCircumstancesForm),
        (FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS, ExplainExceptionalCircumstancesForm),
    ]
    condition_dict = {
        FormSteps.EXCEPTIONAL_CIRCUMSTANCES_REASONS: is_exceptional_circumstances,
    }
    section = "general_application_details"
    section_label = "General application details"
