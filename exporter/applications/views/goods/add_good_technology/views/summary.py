from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.summaries.technology import (
    add_technology_summary_edit_links,
    add_technology_on_application_summary_edit_links,
    technology_summary,
    TECHNOLOGY_ON_APPLICATION_SUMMARY_EDIT_LINKS,
    TECHNOLOGY_SUMMARY_EDIT_LINKS,
    technology_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents
from .mixins import NonFirearmsTechnologyFlagMixin


class BaseTechnologyOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsTechnologyFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/technology/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_technology_summary(self):
        product_summary = technology_summary(
            self.good,
        )
        return product_summary

    def get_technology_on_application_summary(self):
        product_on_application_summary = technology_product_on_application_summary(
            self.good_on_application,
        )
        product_on_application_summary = add_technology_on_application_summary_edit_links(
            product_on_application_summary,
            TECHNOLOGY_ON_APPLICATION_SUMMARY_EDIT_LINKS,
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
            "product_summary": self.get_technology_summary(),
            "product_on_application_summary": self.get_technology_on_application_summary(),
        }


class TechnologyProductOnApplicationSummary(BaseTechnologyOnApplicationSummary):
    summary_type = "technology-on-application-summary"


class TechnologyProductSummary(
    LoginRequiredMixin,
    NonFirearmsTechnologyFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/technology/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = technology_summary(self.good)
        summary = add_technology_summary_edit_links(
            summary,
            TECHNOLOGY_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
