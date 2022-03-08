from django.urls import reverse

from exporter.applications.forms.export_details import export_details_form
from exporter.applications.helpers.date_fields import split_date_into_components, create_formatted_date_from_components
from exporter.applications.services import (
    get_application,
    put_application,
    put_temporary_export_details,
)
from exporter.core.constants import (
    GoodsRecipients,
    GoodsStartingPoint,
    PERMANENT,
    RouteOfGoods,
    TEMPORARY,
    TemporaryOrPermanent,
)
from lite_forms.helpers import get_form_by_pk
from lite_forms.views import MultiFormView

from core.auth.views import LoginRequiredMixin


class ExportDetails(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.success_url = reverse("applications:locations_summary", kwargs={"pk": kwargs["pk"]})
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        is_temporary = request.POST.get("export_type", PERMANENT) == TEMPORARY
        self.forms = export_details_form(
            back_link_url=reverse("applications:task_list", kwargs={"pk": kwargs["pk"]}),
            is_temporary=is_temporary,
        )
        self._action = put_temporary_export_details
        self.data = self._parse_export_details(application)
        self.validate_only_until_final_submission = False
        self.cancel_link_text = "cancel"
        self.cancel_link_url = self.success_url

    @property
    def form_pk(self):
        return int(self.request.POST["form_pk"])

    @property
    def action(self):
        current = get_form_by_pk(self.form_pk, self.forms)
        if current and current.title in [
            GoodsStartingPoint.TITLE,
            TemporaryOrPermanent.TITLE,
            RouteOfGoods.TITLE,
            GoodsRecipients.TITLE,
        ]:
            return put_application

        return self._action

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
    def _parse_export_details(application):
        data = {}

        data["goods_starting_point"] = None
        if application.get("goods_starting_point") is not None:
            data["goods_starting_point"] = application.get("goods_starting_point")

        if data["goods_starting_point"] is not None:
            data["export_type"] = None
            export_type = application.get("export_type")
            if export_type.get("key", "") != "":
                data["export_type"] = export_type

        if data.get("export_type", None) is not None:
            if application.get("temp_export_details") is not None:
                data["temp_export_details"] = application.get("temp_export_details")

            data["is_temp_direct_control"] = None
            if application.get("is_temp_direct_control") is not None:
                data["is_temp_direct_control"] = application.get("is_temp_direct_control")

            proposed_return_date = application.get("proposed_return_date")
            if proposed_return_date:
                # Pre-populate the date fields
                data["year"], data["month"], data["day"] = split_date_into_components(proposed_return_date, "-")

        if data.get("is_temp_direct_control", None) is not None:
            data["is_shipped_waybill_or_lading"] = None
            if application.get("is_shipped_waybill_or_lading") is not None:
                data["is_shipped_waybill_or_lading"] = application.get("is_shipped_waybill_or_lading")

            export_details_text_fields = [
                "temp_direct_control_details",
                "non_waybill_or_lading_route_details",
            ]
            for export_detail in export_details_text_fields:
                application_export_detail = application.get(export_detail)
                if application_export_detail:
                    data[export_detail] = application_export_detail

        if data.get("is_shipped_waybill_or_lading", None) is not None:
            data["goods_recipients"] = None
            if application.get("goods_recipients", None) is not None:
                data["goods_recipients"] = application.get("goods_recipients")

        return data
