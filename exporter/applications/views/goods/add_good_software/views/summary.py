from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.summaries.software import (
    add_software_summary_edit_links,
    software_summary,
    SOFTWARE_SUMMARY_EDIT_LINKS,
    software_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents
from .mixins import NonFirearmsSoftwareFlagMixin


class BaseSoftwareOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsSoftwareFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/software/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_software_summary(self):
        product_summary = software_summary(
            self.good,
        )
        return product_summary

    def get_software_on_application_summary(self):
        product_on_application_summary = software_product_on_application_summary(
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
            "product_summary": self.get_software_summary(),
            "product_on_application_summary": self.get_software_on_application_summary(),
        }


class SoftwareProductOnApplicationSummary(BaseSoftwareOnApplicationSummary):
    summary_type = "software-on-application-summary"


class SoftwareProductSummary(
    LoginRequiredMixin,
    NonFirearmsSoftwareFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/software/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = software_summary(self.good)
        summary = add_software_summary_edit_links(
            summary,
            SOFTWARE_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
