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
)
from exporter.goods.services import edit_technology

from .constants import (
    AddGoodTechnologyToApplicationSteps,
    AddGoodTechnologySteps,
)
from .payloads import (
    TechnologyProductOnApplicationSummaryEditOnwardExportedPayloadBuilder,
    get_onward_incorporated_payload,
)

logger = logging.getLogger(__name__)


class BaseEditView(
    BaseProductEditView,
):
    def get_success_url(self):
        return reverse("applications:technology_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_id, payload):
        return edit_technology(request, good_id, payload)


class BaseTechnologyEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class TechnologySummaryMixin:
    def get_success_url(self):
        return reverse("applications:technology_product_summary", kwargs=self.kwargs)


class EditTechnology:
    @expect_status(
        HTTPStatus.OK,
        "Error editing technology",
        "Unexpected error editing technology",
    )
    def edit_technology(self, request, good_id, payload):
        return edit_technology(request, good_id, payload)

    def run(self, view, form):
        self.edit_technology(
            view.request,
            view.good["id"],
            view.get_step_data(form),
        )


class TechnologyEditName(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    TechnologySummaryMixin,
    StepEditView,
):
    actions = (EditTechnology(),)
    step = ProductNameStep()


class TechnologyEditControlListEntry(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    TechnologySummaryMixin,
    StepEditView,
):
    actions = (EditTechnology(),)
    step = ProductControlListEntryStep()


class TechnologyEditPartNumberView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    TechnologySummaryMixin,
    StepEditView,
):
    actions = (EditTechnology(),)
    step = ProductPartNumberStep()


class BaseTechnologyEditWizardView(
    BaseProductEditWizardView,
):
    def get_success_url(self):
        return reverse("applications:technology_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        return edit_technology(self.request, good_pk, payload)


class TechnologyEditPVGrading(BaseTechnologyEditWizardView):
    form_list = [
        (AddGoodTechnologySteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodTechnologySteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodTechnologySteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodTechnologySteps.PV_GRADING:
            initial = get_pv_grading_initial_data(self.good)
        elif step == AddGoodTechnologySteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodTechnologySteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class TechnologyEditPVGradingDetails(BaseTechnologyEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class TechnologyEditSecurityFeatures(BaseTechnologyEditView):
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


class TechnologyEditDeclaredAtCustoms(BaseTechnologyEditView):
    form_class = ProductDeclaredAtCustomsForm

    def get_initial(self):
        return {
            "has_declared_at_customs": self.good["has_declared_at_customs"],
        }


class TechnologyEditMilitaryUseView(BaseTechnologyEditView):
    form_class = ProductMilitaryUseForm

    def get_initial(self):
        return {
            "is_military_use": self.good["is_military_use"]["key"],
            "modified_military_use_details": self.good["modified_military_use_details"],
        }


class BaseTechnologyEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseTechnologyEditWizardView,
):
    pass


class TechnologyEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseTechnologyEditProductDocumentView,
):
    pass


class TechnologyEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseTechnologyEditProductDocumentView,
):
    pass


class TechnologyEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseTechnologyEditView,
):
    pass


class TechnologyEditProductDescriptionView(
    BaseEditProductDescription,
    BaseTechnologyEditView,
):
    pass


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "technology-on-application-summary",
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
    def edit_technology_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.edit_technology_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_technology_good_on_application_payload(form_dict),
        )

        return redirect(self.get_success_url())


class TechnologyOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodTechnologyToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodTechnologyToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_technology_good_on_application_payload(self, form_dict):
        return TechnologyProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class BaseTechnologyOnApplicationEditView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating technology",
        "Unexpected error updating technology",
    )
    def edit_technology_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_technology_good_on_application(
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


class TechnologyOnApplicationSummaryEditOnwardAltered(BaseTechnologyOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)


class TechnologyOnApplicationSummaryEditOnwardIncorporated(BaseTechnologyOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_onward_incorporated_payload(form)


class TechnologyOnApplicationSummaryEditQuantityValue(BaseTechnologyOnApplicationEditView):
    form_class = ProductQuantityAndValueForm

    def get_initial(self):
        return get_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)
