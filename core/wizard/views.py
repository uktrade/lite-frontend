import logging

from django.views.generic import FormView

from formtools.wizard.views import SessionWizardView

from .storage import NoSaveStorage


logger = logging.getLogger(__name__)


class BaseSessionWizardView(SessionWizardView):
    file_storage = NoSaveStorage()
    template_name = "core/form-wizard.html"

    step_kwargs = {}

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if cleaned_data is None:
            return {}
        return cleaned_data

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)

        try:
            context["title"] = form.get_title()
        except AttributeError:
            pass

        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if self.step_kwargs:
            if self.step_kwargs.get(step):
                step_kwargs = self.step_kwargs[step](self)
                kwargs.update(step_kwargs)
        return kwargs

    def render_to_response(self, context):
        if "title" not in context:
            logger.warning("No title set for `%s`", context["form"].__class__.__name__)
        elif not context["title"]:
            logger.warning("Title set but blank for `%s`", context["form"].__class__.__name__)
        return super().render_to_response(context)


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form_title"] = self.get_form_class().Layout.TITLE
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        step_form_kwargs = self.step.get_form_kwargs(self)
        return {
            **form_kwargs,
            **step_form_kwargs,
        }

    def get_step_data(self, form):
        return self.step.get_step_data(form)
