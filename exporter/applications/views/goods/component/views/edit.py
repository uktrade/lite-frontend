import logging

from http import HTTPStatus

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.applications.services import edit_good_on_application
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_onward_exported,
)
from exporter.applications.views.goods.common.steps import (
    ProductControlListEntryStep,
    ProductNameStep,
    ProductPartNumberStep,
)
from exporter.applications.views.goods.common.edit import (
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
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    get_quantity_and_value_payload,
    ProductEditPVGradingPayloadBuilder,
)
from core.wizard.views import (
    BaseSessionWizardView,
    StepEditView,
)
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
from exporter.goods.forms.goods import ProductIsComponentForm, ProductComponentDetailsForm
from exporter.goods.services import edit_component_accessory

from .constants import (
    AddGoodComponentToApplicationSteps,
    AddGoodComponentSteps,
)
from .payloads import (
    ComponentAccessoryProductOnApplicationSummaryEditOnwardExportedPayloadBuilder,
    ProductEditComponentDetailsPayloadBuilder,
)

from .conditionals import is_component
from .initial import get_is_component_initial_data, get_component_details_initial_data

logger = logging.getLogger(__name__)


class BaseEditView(
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:component_accessory_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_id, payload):
        return edit_component_accessory(request, good_id, payload)


class BaseComponentAccessoryEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class ComponentAccessorySummaryMixin:
    def get_success_url(self):
        return reverse("applications:component_accessory_product_summary", kwargs=self.kwargs)


class EditComponentAccessory:
    @expect_status(
        HTTPStatus.OK,
        "Error editing component/accessory",
        "Unexpected error editing component/accessory",
    )
    def edit_component_accessory(self, request, good_id, payload):
        return edit_component_accessory(request, good_id, payload)

    def run(self, view, form):
        self.edit_component_accessory(
            view.request,
            view.good["id"],
            view.get_step_data(form),
        )


class ComponentAccessoryEditName(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    ComponentAccessorySummaryMixin,
    StepEditView,
):
    actions = (EditComponentAccessory(),)
    step = ProductNameStep()


class ComponentAccessoryEditControlListEntry(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    ComponentAccessorySummaryMixin,
    StepEditView,
):
    actions = (EditComponentAccessory(),)
    step = ProductControlListEntryStep()


class ComponentAccessoryEditPartNumberView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    ComponentAccessorySummaryMixin,
    StepEditView,
):
    actions = (EditComponentAccessory(),)
    step = ProductPartNumberStep()


class BaseComponentAccessoryEditWizardView(
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:component_accessory_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        return edit_component_accessory(self.request, good_pk, payload)


class ComponentAccessoryEditPVGrading(BaseComponentAccessoryEditWizardView):
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


class ComponentAccessoryEditPVGradingDetails(BaseComponentAccessoryEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class ComponentAccessoryEditUsesInformationSecurity(BaseComponentAccessoryEditView):
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


class ComponentAccessoryEditMilitaryUseView(BaseComponentAccessoryEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


class BaseComponentAccessoryEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseComponentAccessoryEditWizardView,
):
    pass


class ComponentAccessoryEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseComponentAccessoryEditProductDocumentView,
):
    pass


class ComponentAccessoryEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseComponentAccessoryEditProductDocumentView,
):
    pass


class ComponentAccessoryEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseComponentAccessoryEditView,
):
    pass


class ComponentAccessoryEditProductDescriptionView(
    BaseEditProductDescription,
    BaseComponentAccessoryEditView,
):
    pass


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "component-accessory-on-application-summary",
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
    def edit_component_accessory_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.edit_component_accessory_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_component_accessory_good_on_application_payload(form_dict),
        )

        return redirect(self.get_success_url())


class ComponentAccessoryOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
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

    def get_edit_component_accessory_good_on_application_payload(self, form_dict):
        return ComponentAccessoryProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class BaseComponentAccessoryOnApplicationEditView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating component accessory",
        "Unexpected error updating component accessory",
    )
    def edit_component_accessory_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_component_accessory_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_payload(form),
        )

    def form_valid(self, form):
        self.perform_actions(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form_title"] = self.form_class.Layout.TITLE
        return context

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class ComponentAccessoryOnApplicationSummaryEditOnwardAltered(BaseComponentAccessoryOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)


class ComponentAccessoryOnApplicationSummaryEditOnwardIncorporated(BaseComponentAccessoryOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        cleaned_data = super().get_edit_payload(form)

        return {
            "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
            **cleaned_data,
        }


class ComponentAccessoryOnApplicationSummaryEditQuantityValue(BaseComponentAccessoryOnApplicationEditView):
    form_class = ProductQuantityAndValueForm

    def get_initial(self):
        return get_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)


class ComponentAccessoryEditComponentDetails(BaseComponentAccessoryEditWizardView):
    form_list = [
        (AddGoodComponentSteps.IS_COMPONENT, ProductIsComponentForm),
        (AddGoodComponentSteps.COMPONENT_DETAILS, ProductComponentDetailsForm),
    ]
    condition_dict = {
        AddGoodComponentSteps.COMPONENT_DETAILS: is_component,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodComponentSteps.IS_COMPONENT:
            initial = get_is_component_initial_data(self.good)
        elif step == AddGoodComponentSteps.COMPONENT_DETAILS and self.good["component_details"]:
            initial = get_component_details_initial_data(self.good)
        return initial

    def get_payload(self, form_dict):
        return ProductEditComponentDetailsPayloadBuilder().build(form_dict)
