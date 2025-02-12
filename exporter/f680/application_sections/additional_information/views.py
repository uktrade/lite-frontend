from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import NotesForCaseOfficerForm


class NotesForCaseOfficersView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.NOTES_FOR_CASEWORKER, NotesForCaseOfficerForm),
    ]
    section = "additional_information"
