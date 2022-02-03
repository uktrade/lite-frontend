from django.urls import reverse

from exporter.applications.forms.temporary_export_details import temporary_export_details_form
from exporter.applications.helpers.date_fields import split_date_into_components, create_formatted_date_from_components
from exporter.applications.services import get_application, put_temporary_export_details
from lite_forms.views import MultiFormView

from core.auth.views import LoginRequiredMixin


class TemporaryExportDetails(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.success_url = reverse("applications:route_of_goods", kwargs={"pk": kwargs["pk"]})
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = temporary_export_details_form(
            back_link_url=reverse("applications:location", kwargs={"pk": kwargs["pk"]})
        )
        self.action = put_temporary_export_details
        self.data = self._parse_temporary_export_details(application)
        self.validate_only_until_final_submission = False
        self.cancel_link_text = "cancel"
        self.cancel_link_url = self.success_url

    def get_validated_data(self):
        data = super().get_validated_data()
        # to ensure date is changed and displayed on the summary list
        if data.get("year") and data.get("month") and data.get("day"):
            data["proposed_return_date"] = create_formatted_date_from_components(data)
        return data

    def prettify_data(self, data):
        data = super().prettify_data(data)
        return data

    @staticmethod
    def _parse_temporary_export_details(application):

        temporary_export_details_text_fields = [
            "temp_export_details",
            "temp_direct_control_details",
        ]

        data = {}

        if application.get("is_temp_direct_control") is not None:
            data["is_temp_direct_control"] = application.get("is_temp_direct_control")

        for temp_export_detail in temporary_export_details_text_fields:
            application_temp_export_detail = application.get(temp_export_detail)
            if application_temp_export_detail:
                data[temp_export_detail] = application_temp_export_detail

        proposed_return_date = application.get("proposed_return_date")
        if proposed_return_date:
            # Pre-populate the date fields
            data["year"], data["month"], data["day"] = split_date_into_components(proposed_return_date, "-")

        return data
