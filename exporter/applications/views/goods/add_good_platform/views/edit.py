import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.conditionals import is_pv_graded
from exporter.applications.views.goods.common.initial import (
    get_control_list_entry_initial_data,
    get_name_initial_data,
    get_pv_grading_initial_data,
    get_pv_grading_details_initial_data,
)
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductNameForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
)
from exporter.goods.forms.goods import ProductUsesInformationSecurityForm
from exporter.goods.services import edit_platform

from .constants import AddGoodPlatformSteps
from .mixins import NonFirearmsFlagMixin


logger = logging.getLogger(__name__)


class BaseEditView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse("applications:platform_summary", kwargs=self.kwargs)

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def form_valid(self, form):
        edit_platform(self.request, self.good["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = reverse("applications:platform_summary", kwargs=self.kwargs)

        return ctx


class BasePlatformEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class PlatformEditName(BasePlatformEditView):
    form_class = ProductNameForm

    def get_initial(self):
        return get_name_initial_data(self.good)


class PlatformEditControlListEntry(BasePlatformEditView):
    form_class = ProductControlListEntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_initial(self):
        return get_control_list_entry_initial_data(self.good)


class BaseEditWizardView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
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

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse("applications:platform_summary", kwargs=self.kwargs)
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_success_url(self):
        return reverse("applications:platform_summary", kwargs=self.kwargs)

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    @expect_status(HTTPStatus.OK, "Error updating firearm", "Unexpected error updating firearm")
    def edit_platform(self, good_pk, form_dict):
        payload = self.get_payload(form_dict)
        return edit_platform(self.request, good_pk, payload)


class PlatformEditPVGrading(BaseEditWizardView):
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

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.edit_platform(self.good["id"], form_dict)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


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
