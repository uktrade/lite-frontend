import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from exporter.applications.constants import F680, OIEL
from exporter.applications.forms.questions import oiel_questions_forms, f680_questions_forms
from exporter.applications.services import put_application, get_application
from lite_forms.views import MultiFormView

from core.auth.views import LoginRequiredMixin


def questions_action(request, pk, data):
    empty_keys = []
    for key in data:
        try:
            # Try to cast to dict if str in order to handle key|value pairs
            data[key] = json.loads(data[key])
            if isinstance(data[key], dict) and "key" in data[key]:
                data[key] = data[key]["key"]
        except (TypeError, ValueError, SyntaxError):
            pass
        if not isinstance(data[key], bool) and not data[key]:
            empty_keys.append(key)

    return put_application(request, pk, data)


class AdditionalInformationFormView(LoginRequiredMixin, MultiFormView):

    case_type_map = {
        "f680": {"class": F680, "forms": f680_questions_forms},
        "oiel": {"class": OIEL, "forms": oiel_questions_forms},
    }

    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.application = get_application(request, self.object_pk)
        case_type = self.application["case_type"]["reference"]["key"]
        self.data = self.get_additional_information(case_type)
        self.forms = self.case_type_map[case_type]["forms"]()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.validate_only_until_final_submission = False

    def prettify_data(self, data):
        data = super().prettify_data(data)
        if data.get("prospect_value"):
            data["prospect_value"] = f"£{intcomma(data['prospect_value'])}"
        return data

    def get_additional_information(self, case_type):
        return {
            field: self.application[field]
            for field in self.case_type_map[case_type]["class"].FIELDS
            if self.application.get(field) is not None
        }
