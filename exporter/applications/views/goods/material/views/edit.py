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
    get_unit_quantity_and_value_initial_data,
)
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    get_unit_quantity_and_value_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.applications.views.goods.common.steps import (
    ProductControlListEntryStep,
    ProductNameStep,
    ProductPartNumberStep,
)
from core.wizard.views import (
    BaseSessionWizardView,
    StepEditView,
)
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductUnitQuantityAndValueForm,
    ProductMilitaryUseForm,
)

from exporter.goods.services import edit_material

from .constants import (
    AddGoodMaterialToApplicationSteps,
    AddGoodMaterialSteps,
)
from .payloads import MaterialProductOnApplicationSummaryEditOnwardExportedPayloadBuilder

logger = logging.getLogger(__name__)


class BaseEditView(
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:material_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_id, payload):
        return edit_material(request, good_id, payload)


class BaseMaterialEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class EditMaterial:
    @expect_status(
        HTTPStatus.OK,
        "Error editing material",
        "Unexpected error editing material",
    )
    def edit_material(self, request, good_id, payload):
        return edit_material(request, good_id, payload)

    def run(self, view, form):
        self.edit_material(
            view.request,
            view.good["id"],
            view.get_step_data(form),
        )


class MaterialSummaryMixin:
    def get_success_url(self):
        return reverse("applications:material_product_summary", kwargs=self.kwargs)


class MaterialEditName(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    MaterialSummaryMixin,
    StepEditView,
):
    actions = (EditMaterial(),)
    step = ProductNameStep()


class MaterialEditControlListEntry(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    MaterialSummaryMixin,
    StepEditView,
):
    actions = (EditMaterial(),)
    step = ProductControlListEntryStep()


class MaterialEditPartNumberView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    MaterialSummaryMixin,
    StepEditView,
):
    actions = (EditMaterial(),)
    step = ProductPartNumberStep()


class BaseMaterialEditWizardView(
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:material_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        return edit_material(self.request, good_pk, payload)


class MaterialEditPVGrading(BaseMaterialEditWizardView):
    form_list = [
        (AddGoodMaterialSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodMaterialSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodMaterialSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodMaterialSteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodMaterialSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodMaterialSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class MaterialEditPVGradingDetails(BaseMaterialEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class MaterialEditMilitaryUseView(BaseMaterialEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


class BaseMaterialEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseMaterialEditWizardView,
):
    pass


class MaterialEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseMaterialEditProductDocumentView,
):
    pass


class MaterialEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseMaterialEditProductDocumentView,
):
    pass


class MaterialEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseMaterialEditView,
):
    pass


class MaterialEditProductDescriptionView(
    BaseEditProductDescription,
    BaseMaterialEditView,
):
    pass


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "material-on-application-summary",
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


class BaseMaterialOnApplicationSummaryEditWizardView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    BaseSessionWizardView,
):
    @expect_status(
        HTTPStatus.OK,
        "Error updating material",
        "Unexpected error updating material",
    )
    def edit_material_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.edit_material_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_material_good_on_application_payload(form_dict),
        )

        return redirect(self.get_success_url())


class MaterialOnApplicationSummaryEditOnwardExported(BaseMaterialOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodMaterialToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodMaterialToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodMaterialToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_material_good_on_application_payload(self, form_dict):
        return MaterialProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class BaseMaterialOnApplicationEditView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating material",
        "Unexpected error updating material",
    )
    def edit_Material_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_Material_good_on_application(
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


class MaterialOnApplicationSummaryEditOnwardAltered(BaseMaterialOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)


class MaterialOnApplicationSummaryEditOnwardIncorporated(BaseMaterialOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        cleaned_data = super().get_edit_payload(form)

        return {
            "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
            **cleaned_data,
        }


class MaterialOnApplicationSummaryEditUnitQuantityValue(BaseMaterialOnApplicationEditView):
    form_class = ProductUnitQuantityAndValueForm

    def get_initial(self):
        return get_unit_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_unit_quantity_and_value_payload(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}
