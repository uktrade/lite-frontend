from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin, GoodOnApplicationMixin
from exporter.applications.summaries.platform import (
    add_platform_summary_edit_links,
    platform_summary,
    PLATFORM_SUMMARY_EDIT_LINKS,
    platform_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents

from .mixins import NonFirearmsFlagMixin


class BasePlatformOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/platform/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_platform_summary(self):
        product_summary = platform_summary(
            self.good,
        )
        return product_summary

    def get_platform_on_application_summary(self):
        product_on_application_summary = platform_product_on_application_summary(
            self.good_on_application,
        )
        return product_on_application_summary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            "application": self.application,
            "good": self.good,
            "good_on_application": self.good_on_application,
            "product_summary": self.get_platform_summary(),
            "product_on_application_summary": self.get_platform_on_application_summary(),
        }


class PlatformProductOnApplicationSummary(BasePlatformOnApplicationSummary):
    summary_type = "platform-on-application-summary"


class PlatformSummary(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/platform/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = platform_summary(self.good)
        summary = add_platform_summary_edit_links(
            summary,
            PLATFORM_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
