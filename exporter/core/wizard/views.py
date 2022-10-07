from django.views.generic import FormView

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


class StepEditView(FormView):
    template_name = "core/form.html"

    def get_form_class(self):
        return self.step.form_class

    def get_initial(self):
        return self.step.get_initial(self)

    def form_valid(self, form):
        for action in self.actions:
            action.run(self, form)
        return super().form_valid(form)
