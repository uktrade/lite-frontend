from http import HTTPStatus
from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from exporter.f680.services import patch_f680_application, get_f680_application
from exporter.f680.payloads import F680PatchPayloadBuilder, F680AppendingPayloadBuilder
from exporter.f680.views import F680FeatureRequiredMixin


class F680ApplicationSectionWizard(LoginRequiredMixin, F680FeatureRequiredMixin, BaseSessionWizardView):
    form_list = []
    condition_dict = {}
    section = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application, _ = self.get_f680_application(kwargs["pk"])

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving F680 application",
        "Unexpected error retrieving F680 application",
        reraise_404=True,
    )
    def get_f680_application(self, pk):
        return get_f680_application(self.request, pk)

    @expect_status(
        HTTPStatus.OK,
        "Error updating F680 application",
        "Unexpected error updating F680 application",
    )
    def patch_f680_application(self, data):
        if self.section == "general_application_details":
            data["name"] = data["application"]["sections"]["general_application_details"]["fields"]["name"]["answer"]
        return patch_f680_application(self.request, self.application["id"], data)

    def deserialize(self, value, datatype):
        if datatype == "date":
            return datetime.fromisoformat(value)
        return value

    def deserialize_payload(self, payload):
        data = {}
        for field in payload["fields"].values():
            key = field["key"]
            data[key] = self.deserialize(field["raw_answer"], field["datatype"])
        return data

    def get_form_initial(self, step):
        if not self.application.get("application", {}).get("sections", {}).get(self.section):
            return {}

        return self.deserialize_payload(self.application["application"]["sections"][self.section])

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",
            kwargs={
                "pk": application_id,
            },
        )

    def get_back_link_url(self):
        return self.get_success_url(self.application["id"])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["back_link_url"] = self.get_back_link_url()
        return context_data

    def get_payload(self, form_dict):
        current_application = self.application.get("application", {})
        return F680PatchPayloadBuilder().build(self.section, self.section_label, current_application, form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.patch_f680_application(data)
        return redirect(self.get_success_url(response_data["id"]))


class F680MultipleItemApplicationSectionWizard(F680ApplicationSectionWizard):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.id = None
        if "id" in kwargs:
            self.id = str(kwargs["id"])

    def get_form_initial(self, step):
        if not self.id:
            return {}

        all_items = self.application["application"]["sections"][self.section]["items"]
        existing_items = {item["id"]: item for item in all_items}
        item = existing_items[self.id]
        return self.deserialize_payload(item)

    def get_payload(self, form_dict):
        current_application = self.application.get("application", {})
        return F680AppendingPayloadBuilder().build(
            self.section, self.section_label, current_application, form_dict, self.id
        )
