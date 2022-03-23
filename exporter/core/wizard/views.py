from formtools.wizard.views import SessionWizardView

from .storage import NoSaveStorage


class BaseSessionWizardView(SessionWizardView):
    file_storage = NoSaveStorage()
    template_name = "core/form-wizard.html"
