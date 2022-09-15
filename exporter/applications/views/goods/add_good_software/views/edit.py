import logging

from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin
from exporter.applications.services import edit_good_on_application
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_onward_exported,
)
from exporter.applications.views.goods.common.edit import (
    BaseEditControlListEntry,
    BaseEditName,
    BaseEditPartNumber,
    BaseEditProductDescription,
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
    get_quantity_and_value_initial_data,
)
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    get_quantity_and_value_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductMilitaryUseForm,
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductQuantityAndValueForm,
)
from exporter.goods.forms import (
    ProductSecurityFeaturesForm,
    ProductDeclaredAtCustomsForm,
    ProductDesignDetailsForm,
)
from exporter.goods.services import edit_software

from .constants import (
    AddGoodSoftwareToApplicationSteps,
    AddGoodSoftwareSteps,
)
from .payloads import (
    SoftwareProductOnApplicationSummaryEditOnwardExportedPayloadBuilder,
    get_onward_incorporated_payload,
)
from .mixins import NonFirearmsSoftwareFlagMixin

logger = logging.getLogger(__name__)


class BaseEditView(
    NonFirearmsSoftwareFlagMixin,
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:software_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_id, payload):
        edit_software(request, good_id, payload)


class BaseSoftwareEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class SoftwareEditName(BaseEditName, BaseSoftwareEditView):
    pass


class SoftwareEditControlListEntry(BaseEditControlListEntry, BaseSoftwareEditView):
    pass


class SoftwareEditPartNumberView(
    BaseEditPartNumber,
    BaseSoftwareEditView,
):
    pass


class BaseSoftwareEditWizardView(
    NonFirearmsSoftwareFlagMixin,
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:software_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_pk, payload):
        return edit_software(self.request, good_pk, payload)


class SoftwareEditPVGrading(BaseSoftwareEditWizardView):
    form_list = [
        (AddGoodSoftwareSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodSoftwareSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodSoftwareSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodSoftwareSteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodSoftwareSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodSoftwareSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class SoftwareEditPVGradingDetails(BaseSoftwareEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class SoftwareEditSecurityFeatures(BaseSoftwareEditView):
    form_class = ProductSecurityFeaturesForm

    def get_initial(self):
        if self.good["has_security_features"]:
            return {
                "has_security_features": self.good["has_security_features"],
                "security_feature_details": self.good["security_feature_details"],
            }

        return {
            "has_security_features": self.good["has_security_features"],
        }


class SoftwareEditDeclaredAtCustoms(BaseSoftwareEditView):
    form_class = ProductDeclaredAtCustomsForm

    def get_initial(self):
        return {
            "has_declared_at_customs": self.good["has_declared_at_customs"],
        }


class SoftwareEditDesignDetails(BaseSoftwareEditView):
    form_class = ProductDesignDetailsForm

    def get_initial(self):
        return {
            "design_details": self.good["design_details"],
        }


class SoftwareEditMilitaryUseView(BaseSoftwareEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


class BaseSoftwareEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseSoftwareEditWizardView,
):
    pass


class SoftwareEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseSoftwareEditProductDocumentView,
):
    pass


class SoftwareEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseSoftwareEditProductDocumentView,
):
    pass


class SoftwareEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseSoftwareEditView,
):
    pass


class SoftwareEditProductDescriptionView(
    BaseEditProductDescription,
    BaseSoftwareEditView,
):
    pass


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "software-on-application-summary",
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
    NonFirearmsSoftwareFlagMixin,
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
    def edit_software_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_software_good_on_application(
                self.request,
                self.good_on_application["id"],
                self.get_edit_software_good_on_application_payload(form_dict),
            )
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class SoftwareOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodSoftwareToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodSoftwareToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_software_good_on_application_payload(self, form_dict):
        return SoftwareProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class BaseSoftwareOnApplicationEditView(
    LoginRequiredMixin,
    NonFirearmsSoftwareFlagMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating software",
        "Unexpected error updating software",
    )
    def edit_software_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_software_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_payload(form),
        )

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise service_error
        return error_page(self.request, service_error.user_message)

    def form_valid(self, form):
        try:
            self.perform_actions(form)
        except ServiceError as e:
            return self.handle_service_error(e)

        return super().form_valid(form)

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class SoftwareOnApplicationSummaryEditOnwardAltered(BaseSoftwareOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)


class SoftwareOnApplicationSummaryEditOnwardIncorporated(BaseSoftwareOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_onward_incorporated_payload(form)


class SoftwareOnApplicationSummaryEditQuantityValue(BaseSoftwareOnApplicationEditView):
    form_class = ProductQuantityAndValueForm

    def get_initial(self):
        return get_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)
