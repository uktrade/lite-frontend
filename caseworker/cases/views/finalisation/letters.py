from caseworker.cases.views.finalisation.forms import SelectInformLetterTemplateForm

from django.views.generic import FormView
from caseworker.letter_templates.services import get_letter_templates, get_letter_template

from core.auth.views import LoginRequiredMixin
from core.helpers import convert_dict_to_query_params


class SelectInformTemplate(LoginRequiredMixin, FormView):

    template_name = "core/form.html"
    form_class = SelectInformLetterTemplateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1), "decision": "refuse"}

        self.templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))
        inform_template_id = self.templates["results"][0]["id"]

        template_details = get_letter_template(self.request, inform_template_id)

        context[""] = {}

        return context
