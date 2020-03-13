from django.urls import reverse_lazy

from applications.forms.end_use_details import end_use_details_form
from applications.services import put_application, get_application
from lite_content.lite_exporter_frontend.applications import EndUseDetails as strings
from lite_forms.views import SummaryListFormView


class EndUseDetails(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = end_use_details_form(application, request)
        self.action = put_application
        self.data = self._parse_end_use_details(application)
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = strings.EndUseDetailsSummaryList.TITLE
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = "Save and continue"

    @staticmethod
    def _parse_end_use_details(application):

        end_use_details = [
            "military_end_use_controls",
            "informed_wmd",
            "suspected_wmd",
            "eu_military",
            "compliant_limitations_eu",
        ]

        data = {}
        for end_use_detail in end_use_details:
            end_use_question = "is_" + end_use_detail
            end_use_reference = end_use_detail + "_ref"

            application_end_use_question = application.get(end_use_question)
            if application_end_use_question is not None:
                data[end_use_question] = application_end_use_question

            application_end_use_reference = application.get(end_use_reference)
            if application_end_use_reference:
                data[end_use_reference] = application_end_use_reference

        return data
