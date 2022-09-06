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
    ProductUsesInformationSecurityForm,
)
from exporter.goods.services import edit_component

from .constants import (
    AddGoodComponentToApplicationSteps,
    AddGoodComponentSteps,
)
from .payloads import ComponentProductOnApplicationSummaryEditOnwardExportedPayloadBuilder
from .mixins import NonFirearmsComponentFlagMixin

logger = logging.getLogger(__name__)


class BaseEditView(
    NonFirearmsComponentFlagMixin,
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:component_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_id, payload):
        edit_component(request, good_id, payload)


class BaseComponentEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class ComponentEditName(BaseEditName, BaseComponentEditView):
    pass


class ComponentEditControlListEntry(BaseEditControlListEntry, BaseComponentEditView):
    pass


class ComponentEditPartNumberView(
    BaseEditPartNumber,
    BaseComponentEditView,
):
    pass


class BaseComponentEditWizardView(
    NonFirearmsComponentFlagMixin,
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:component_product_summary", kwargs=self.kwargs)

    def edit_object(self, request, good_pk, payload):
        return edit_component(self.request, good_pk, payload)


class ComponentEditPVGrading(BaseComponentEditWizardView):
    form_list = [
        (AddGoodComponentSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodComponentSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodComponentSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodComponentSteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodComponentSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodComponentSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class ComponentEditPVGradingDetails(BaseComponentEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class ComponentEditUsesInformationSecurity(BaseComponentEditView):
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


class ComponentEditMilitaryUseView(BaseComponentEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


class BaseComponentEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseComponentEditWizardView,
):
    pass


class ComponentEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseComponentEditProductDocumentView,
):
    pass


class ComponentEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseComponentEditProductDocumentView,
):
    pass


class ComponentEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseComponentEditView,
):
    pass


class ComponentEditProductDescriptionView(
    BaseEditProductDescription,
    BaseComponentEditView,
):
    pass


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "component-on-application-summary",
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
    NonFirearmsComponentFlagMixin,
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
    def edit_component_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_component_good_on_application(
                self.request,
                self.good_on_application["id"],
                self.get_edit_component_good_on_application_payload(form_dict),
            )
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class ComponentOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodComponentToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodComponentToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_component_good_on_application_payload(self, form_dict):
        return ComponentProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class BaseComponentOnApplicationEditView(
    LoginRequiredMixin,
    NonFirearmsComponentFlagMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating component",
        "Unexpected error updating component",
    )
    def edit_component_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_component_good_on_application(
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


class ComponentOnApplicationSummaryEditOnwardAltered(BaseComponentOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)


class ComponentOnApplicationSummaryEditOnwardIncorporated(BaseComponentOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        cleaned_data = super().get_edit_payload(form)

        return {
            "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
            **cleaned_data,
        }


class ComponentOnApplicationSummaryEditQuantityValue(BaseComponentOnApplicationEditView):
    form_class = ProductQuantityAndValueForm

    def get_initial(self):
        return get_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)
