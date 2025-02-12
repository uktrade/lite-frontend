from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import NotesForCaseOfficerForm


class NotesForCaseOfficersView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.NOTES_FOR_CASEWORKER, NotesForCaseOfficerForm),
    ]
    section = "additional_information"
    # template_name = "applications/case-notes.html"

    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form, **kwargs)
    #     notes = get_case_notes(self.request, self.application["id"])["case_notes"]
    #     return {
    #         **context,
    #         "application": self.application,
    #         "notes": notes,
    #         "post_url": reverse_lazy("applications:notes", kwargs={"pk": self.application["id"]}),
    #         "error": kwargs.get("error"),
    #         "text": kwargs.get("text", ""),
    #     }
