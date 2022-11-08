from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.summaries.platform import (
    add_complete_item_summary_edit_links,
    add_complete_item_on_application_summary_edit_links,
    COMPLETE_ITEM_ON_APPLICATION_SUMMARY_EDIT_LINKS,
    complete_item_summary,
    COMPLETE_ITEM_SUMMARY_EDIT_LINKS,
    complete_item_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents
from .mixins import NonFirearmsPlatformFlagMixin


class BasePlatformOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsPlatformFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/platform/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_complete_item_summary(self):
        product_summary = complete_item_summary(
            self.good,
        )
        return product_summary

    def get_complete_item_on_application_summary(self):
        product_on_application_summary = complete_item_product_on_application_summary(
            self.good_on_application,
        )
        product_on_application_summary = add_complete_item_on_application_summary_edit_links(
            product_on_application_summary,
            COMPLETE_ITEM_ON_APPLICATION_SUMMARY_EDIT_LINKS,
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
            "product_summary": self.get_complete_item_summary(),
            "product_on_application_summary": self.get_complete_item_on_application_summary(),
        }


class PlatformProductOnApplicationSummary(BasePlatformOnApplicationSummary):
    summary_type = "complete_item-on-application-summary"


class PlatformProductSummary(
    LoginRequiredMixin,
    NonFirearmsPlatformFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/platform/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = complete_item_summary(self.good)
        summary = add_complete_item_summary_edit_links(
            summary,
            COMPLETE_ITEM_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
