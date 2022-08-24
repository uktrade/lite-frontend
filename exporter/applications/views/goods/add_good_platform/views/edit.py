import logging

from http import HTTPStatus

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from exporter.applications.services import edit_platform_good_on_application
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_onward_exported,
)
from exporter.applications.views.goods.common.edit import (
    BaseEditControlListEntry,
    BaseEditName,
    BaseEditPartNumber,
    BaseEditProductDocumentAvailability,
    BaseEditProductDocumentSensitivity,
    BaseEditProductDocumentView,
    BaseProductDocumentUpload,
    BaseProductEditView,
    BaseProductEditWizardView,
)
from exporter.applications.views.goods.common.initial import (
    get_is_onward_exported_initial_data,
    get_onward_altered_processed_initial_data,
    get_onward_incorporated_initial_data,
    get_pv_grading_initial_data,
    get_pv_grading_details_initial_data,
)
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodOnApplicationMixin,
    NonFirearmsFlagMixin,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
)
from exporter.goods.forms.goods import (
    ProductMilitaryUseForm,
    ProductUsesInformationSecurityForm,
)
from exporter.goods.services import edit_platform

from .constants import (
    AddGoodPlatformToApplicationSteps,
    AddGoodPlatformSteps,
)
from .payloads import PlatformProductOnApplicationSummaryEditOnwardExportedPayloadBuilder


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


class PlatformEditPartNumberView(
    BaseEditPartNumber,
    BasePlatformEditView,
):
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


class PlatformEditMilitaryUseView(BasePlatformEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


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


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "platform-on-application-summary",
    ]

    def dispatch(self, request, *args, **kwargs):
        if kwargs["summary_type"] not in self.SUMMARY_TYPES:
            raise Http404("Not a valid summary type")

        return super().dispatch(request, *args, **kwargs)

    def get_summary_url(self):
        summary_url_name = self.kwargs["summary_type"].replace("-", "_")

        return reverse(
            f"applications:{summary_url_name}",
            kwargs={
                "pk": self.application["id"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_success_url(self):
        return self.get_summary_url()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["back_link_url"] = self.get_summary_url()

        return ctx


class BaseProductOnApplicationSummaryEditWizardView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    BaseSessionWizardView,
):
    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_platform_good_on_application(self, request, good_on_application_id, payload):
        return edit_platform_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_platform_good_on_application(
                self.request,
                self.good_on_application["id"],
                self.get_edit_platform_good_on_application_payload(form_dict),
            )
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class PlatformOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodPlatformToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodPlatformToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodPlatformToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodPlatformToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_platform_good_on_application_payload(self, form_dict):
        return PlatformProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)
