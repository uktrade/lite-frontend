from django.views.generic import FormView
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import ApplicationMixin
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from exporter.applications.services import put_application

from .forms import F680ReferenceNumberForm
from .mixins import NonF680SecurityClassifiedFlagMixin


class BaseApplicationEditView(
    LoginRequiredMixin,
    NonF680SecurityClassifiedFlagMixin,
    ApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_back_link_url(self):
        return self.get_success_url()

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def get_success_url(self):
        return reverse(
            "applications:application_export_details_summary",
            kwargs={"pk": self.application["id"]},
        )

    def edit_object(self, request, application_id, payload):
        put_application(request, application_id, payload)

    def form_valid(self, form):
        self.edit_object(self.request, self.application["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = self.get_back_link_url()
        ctx["title"] = self.form_class.Layout.TITLE

        return ctx


class EditExportDetailsF680ReferenceNumber(BaseApplicationEditView):
    form_class = F680ReferenceNumberForm

    def get_initial(self):
        return {"f680_reference_number": self.application["f680_reference_number"]}

    def get_edit_payload(self, form):
        return get_cleaned_data(form)
