import json

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from applications.constants import F680
from applications.forms.questions import questions_forms
from applications.services import put_application, get_application
from core.helpers import str_to_bool
from lite_content.lite_exporter_frontend import applications
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, data):
    if str_to_bool(data.get("expedited", False)):
        if "year" in data and "month" in data and "day" in data:
            data["expedited_date"] = f"{data['year']}-{str(data['month']).zfill(2)}-{str(data['day']).zfill(2)}"

    else:
        if "expedited_date" in data:
            del data["expedited_date"]
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


class AdditionalInformationFormView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.data = self.get_additional_information(request, self.object_pk)
        self.forms = questions_forms()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = applications.F680ClearanceTaskList.ADDITIONAL_INFORMATION
        self.summary_list_notice_title = applications.F680ClearanceTaskList.NOTICE_TITLE
        self.summary_list_notice_text = applications.F680ClearanceTaskList.NOTICE_TEXT
        self.summary_list_button = applications.F680ClearanceTaskList.SAVE_AND_RETURN
        self.validate_only_until_final_submission = False

    def prettify_data(self, data):
        data = super().prettify_data(data)
        if "prospect_value" in data and data["prospect_value"]:
            data["prospect_value"] = f"£{intcomma(data['prospect_value'])}"
        return data

    @staticmethod
    def get_additional_information(request, application_id):
        application = get_application(request, application_id)
        return {field: application[field] for field in F680.FIELDS if application.get(field) is not None}
