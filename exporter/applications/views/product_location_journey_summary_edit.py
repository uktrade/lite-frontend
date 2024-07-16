from core.auth.views import LoginRequiredMixin
from exporter.applications.forms import product_location_journey_summary_edit
from exporter.applications.helpers.date_fields import split_date_into_components
from exporter.applications.views.goods.common.mixins import ApplicationMixin
from exporter.applications.services import put_application, put_temporary_export_details
from django.views.generic import FormView
from django.urls import reverse
from django.shortcuts import redirect


class TemporaryExportDetailsView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "export_details_edit.html"
    form_class = product_location_journey_summary_edit.TemporaryExportDetailsForm

    def get_initial(self):
        initial = super().get_initial()
        initial["temp_export_details"] = self.application["temp_export_details"]
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]})
        context["form_title"] = self.form_class.Layout.TITLE

        return context

    def form_valid(self, form):
        put_temporary_export_details(self.request, self.kwargs["pk"], form.cleaned_data)

        return redirect(reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]}))


class TemporaryDirectControlView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "direct_control_edit.html"
    form_class = product_location_journey_summary_edit.TemporaryDirectControlForm

    def get_initial(self):
        initial = super().get_initial()
        initial["is_temp_direct_control"] = self.application["is_temp_direct_control"]
        initial["temp_direct_control_details"] = self.application.get("temp_direct_control_details") or ""
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]})
        context["form_title"] = "Will the products remain under your direct control while overseas?"
        return context

    def form_valid(self, form):
        data, status_code = put_temporary_export_details(self.request, self.kwargs["pk"], form.cleaned_data)

        if status_code == 400:
            # Extract and add errors to the form
            errors = data.get("errors", {})
            for field, error_list in errors.items():
                for error in error_list:
                    form.add_error(field, error)
            return self.form_invalid(form)

        return redirect(reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]}))


class ProposedReturnDateView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "export_details_edit.html"
    form_class = product_location_journey_summary_edit.ProposedReturnDateForm

    def get_initial(self):
        initial = super().get_initial()
        proposed_return_date = self.application["proposed_return_date"]
        initial["year"], initial["month"], initial["day"] = split_date_into_components(proposed_return_date, "-")
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]})
        context["form_title"] = self.form_class.Layout.TITLE

        return context

    def form_valid(self, form):
        data, status_code = put_temporary_export_details(self.request, self.kwargs["pk"], form.cleaned_data)

        if status_code == 400:
            errors = data.get("errors", {})
            for field, error_list in errors.items():
                for error in error_list:
                    form.add_error(field, error)
            return self.form_invalid(form)

        return redirect(reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]}))


class ShippedWaybillOrLadingView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "shipped_waybill_lading_edit.html"
    form_class = product_location_journey_summary_edit.ShippedWaybillOrLadingViewForm

    def get_initial(self):
        initial = super().get_initial()
        initial["is_shipped_waybill_or_lading"] = self.application["is_shipped_waybill_or_lading"]
        initial["non_waybill_or_lading_route_details"] = (
            self.application.get("non_waybill_or_lading_route_details") or ""
        )
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]})
        context["form_title"] = "Are the products being shipped from the UK on an air waybill or bill of lading?"
        return context

    def form_valid(self, form):
        data, status_code = put_application(self.request, self.kwargs["pk"], form.cleaned_data)

        if status_code == 400:
            errors = data.get("errors", {})
            for field, error_list in errors.items():
                for error in error_list:
                    form.add_error(field, error)
            return self.form_invalid(form)

        return redirect(reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]}))
