from django.urls import reverse
from django.views.generic import TemplateView

from exporter.applications.forms.end_use_details import end_use_details_form
from exporter.applications.services import put_end_use_details, get_application
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import EndUseDetails as strings
from lite_forms.views import SummaryListFormView

from core.auth.views import LoginRequiredMixin


class EndUseDetails(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.object_pk = kwargs["pk"]
        self.application = get_application(request, self.object_pk)
        self.success_url = reverse("applications:task_list", kwargs={"pk": self.object_pk}) + "#end_use_details"
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_view = self._get_form_view(request, **kwargs)
        return form_view.get(request, back_link=self.success_url, **kwargs)

    def post(self, request, **kwargs):
        form_view = self._get_form_view(request, **kwargs)
        return form_view.post(request, **kwargs)

    def _get_form_view(self, request, **kwargs):
        # Construct an override init method for the class instance
        def init(request, **kwargs):
            pass

        summary_list_form_view = SummaryListFormView()
        summary_list_form_view.back_url = self.success_url
        summary_list_form_view.back_link_text = "Back to application overview"

        summary_list_form_view.instruction_text = "Review your answers below and make any amends you need to. Click 'Save and continue' to save your progress."

        summary_list_form_view.init = init
        summary_list_form_view.request = request
        summary_list_form_view.kwargs = kwargs

        summary_list_form_view.object_pk = self.object_pk
        summary_list_form_view.summary_list_title = strings.EndUseDetailsSummaryList.TITLE
        summary_list_form_view.summary_list_notice_title = ""
        summary_list_form_view.summary_list_notice_text = ""
        summary_list_form_view.summary_list_button = generic.SAVE_AND_CONTINUE
        summary_list_form_view.forms = end_use_details_form(
            application=self.application, request=request, back_link=self.success_url
        )
        summary_list_form_view.action = put_end_use_details
        summary_list_form_view.success_url = self.success_url
        summary_list_form_view.data = self._parse_end_use_details()
        summary_list_form_view.validate_only_until_final_submission = False

        return summary_list_form_view

    def _parse_end_use_details(self):
        end_use_linked_details = [
            "military_end_use_controls",
            "informed_wmd",
            "suspected_wmd",
            "eu_military",
            "compliant_limitations_eu",
        ]

        data = {}
        for end_use_detail in end_use_linked_details:
            end_use_question = "is_" + end_use_detail
            end_use_reference = end_use_detail + "_ref"

            application_end_use_question = self.application.get(end_use_question)
            if application_end_use_question is not None:
                data[end_use_question] = application_end_use_question

            application_end_use_reference = self.application.get(end_use_reference)
            if application_end_use_reference:
                data[end_use_reference] = application_end_use_reference

        intended_end_use = self.application.get("intended_end_use")
        if intended_end_use:
            data["intended_end_use"] = intended_end_use

        return data
