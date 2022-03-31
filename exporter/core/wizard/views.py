from formtools.wizard.views import SessionWizardView

from .storage import NoSaveStorage


class BaseSessionWizardView(SessionWizardView):
    file_storage = NoSaveStorage()
    template_name = "core/form-wizard.html"

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if cleaned_data is None:
            return {}
        return cleaned_data
