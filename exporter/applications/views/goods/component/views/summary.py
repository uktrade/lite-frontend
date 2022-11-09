from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.summaries.component import (
    add_component_accessory_summary_edit_links,
    add_component_accessory_on_application_summary_edit_links,
    COMPONENT_ACCESSORY_ON_APPLICATION_SUMMARY_EDIT_LINKS,
    component_accessory_summary,
    COMPONENT_ACCESSORY_SUMMARY_EDIT_LINKS,
    component_accessory_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents
from .mixins import NonFirearmsComponentFlagMixin


class BaseComponentOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsComponentFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/component/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_component_accessory_summary(self):
        product_summary = component_accessory_summary(
            self.good,
        )
        return product_summary

    def get_component_accessory_on_application_summary(self):
        product_on_application_summary = component_accessory_product_on_application_summary(
            self.good_on_application,
        )
        product_on_application_summary = add_component_accessory_on_application_summary_edit_links(
            product_on_application_summary,
            COMPONENT_ACCESSORY_ON_APPLICATION_SUMMARY_EDIT_LINKS,
            self.application,
            self.good_on_application,
            self.summary_type,
        )
        return product_on_application_summary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "application": self.application,
            "good": self.good,
            "good_on_application": self.good_on_application,
            "product_summary": self.get_component_accessory_summary(),
            "product_on_application_summary": self.get_component_accessory_on_application_summary(),
        }


class ComponentProductOnApplicationSummary(BaseComponentOnApplicationSummary):
    summary_type = "component-accessory-on-application-summary"


class ComponentProductSummary(
    LoginRequiredMixin,
    NonFirearmsComponentFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/component/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = component_accessory_summary(self.good)
        summary = add_component_accessory_summary_edit_links(
            summary,
            COMPONENT_ACCESSORY_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
