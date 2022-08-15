import logging

from django.urls import reverse

from exporter.applications.views.goods.common.conditionals import is_pv_graded
from exporter.applications.views.goods.common.edit import (
    BaseEditControlListEntry,
    BaseEditName,
    BaseEditProductDocumentAvailability,
    BaseEditProductDocumentSensitivity,
    BaseEditProductDocumentView,
    BaseProductDocumentUpload,
    BaseProductEditView,
    BaseProductEditWizardView,
)
from exporter.applications.views.goods.common.initial import (
    get_pv_grading_initial_data,
    get_pv_grading_details_initial_data,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.goods.forms.common import (
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
)
from exporter.goods.forms.goods import ProductUsesInformationSecurityForm
from exporter.goods.services import edit_platform

from .constants import AddGoodPlatformSteps
from .mixins import NonFirearmsFlagMixin


logger = logging.getLogger(__name__)


class BaseEditView(
    NonFirearmsFlagMixin,
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:platform_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_id, payload):
        edit_platform(request, good_id, payload)


class BasePlatformEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class PlatformEditName(BaseEditName, BasePlatformEditView):
    pass


class PlatformEditControlListEntry(BaseEditControlListEntry, BasePlatformEditView):
    pass


class BasePlatformEditWizardView(
    NonFirearmsFlagMixin,
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:platform_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_pk, payload):
        return edit_platform(self.request, good_pk, payload)


class PlatformEditPVGrading(BasePlatformEditWizardView):
    form_list = [
        (AddGoodPlatformSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodPlatformSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodPlatformSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodPlatformSteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodPlatformSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodPlatformSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class PlatformEditPVGradingDetails(BasePlatformEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class PlatformEditUsesInformationSecurity(BasePlatformEditView):
    form_class = ProductUsesInformationSecurityForm

    def get_initial(self):
        if not self.good["uses_information_security"]:
            return {
                "uses_information_security": self.good["uses_information_security"],
            }

        return {
            "uses_information_security": self.good["uses_information_security"],
            "information_security_details": self.good["information_security_details"],
        }

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class BasePlatformEditProductDocumentView(
    BaseEditProductDocumentView,
    BasePlatformEditWizardView,
):
    pass


class PlatformEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BasePlatformEditProductDocumentView,
):
    pass


class PlatformEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BasePlatformEditProductDocumentView,
):
    pass


class PlatformEditProductDocumentView(
    BaseProductDocumentUpload,
    BasePlatformEditView,
):
    pass
