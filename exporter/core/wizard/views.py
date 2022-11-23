from django.shortcuts import redirect
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

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        step_form_kwargs = self.step.get_form_kwargs(self)
        return {
            **form_kwargs,
            **step_form_kwargs,
        }

    def get_step_data(self, form):
        return self.step.get_step_data(form)


class StepSessionWizardView(BaseSessionWizardView):
    step_dict = None

    @classmethod
    def get_initkwargs(
        cls,
        *args,
        **kwargs,
    ):
        form_list = [(step.name, step.form_class) for step in cls.step_list]
        step_dict = {step.name: step for step in cls.step_list}
        return BaseSessionWizardView.get_initkwargs(
            form_list=form_list,
            step_dict=step_dict,
            *args,
            **kwargs,
        )

    def get_form_initial(self, step):
        step_obj = self.step_dict[step]  # pylint: disable=unsubscriptable-object

        return step_obj.get_initial(self)

    def get_form_kwargs(self, step=None):
        step_obj = self.step_dict[step]  # pylint: disable=unsubscriptable-object

        return step_obj.get_form_kwargs(self)

    def process_forms(self, form_list, form_dict, **kwargs):
        self.edit_object(self.request, self.good["id"], self.get_payload(form_dict))

    def done(self, form_list, form_dict, **kwargs):
        self.process_forms(form_list, form_dict, **kwargs)

        return redirect(self.get_success_url())
