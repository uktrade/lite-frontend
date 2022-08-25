from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from .mixins import NonFirearmsMaterialFlagMixin

from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin, GoodOnApplicationMixin
from exporter.applications.summaries.material import (
    add_material_summary_edit_links,
    material_summary,
    MATERIAL_SUMMARY_EDIT_LINKS,
    material_product_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents


class BaseMaterialOnApplicationSummary(
    LoginRequiredMixin,
    NonFirearmsMaterialFlagMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/material/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_material_summary(self):
        product_summary = material_summary(
            self.good,
        )
        return product_summary

    def get_material_on_application_summary(self):
        product_on_application_summary = material_product_on_application_summary(
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
            "product_summary": self.get_Materials_summary(),
            "product_on_application_summary": self.get_material_on_application_summary(),
        }


class MaterialProductOnApplicationSummary(BaseMaterialOnApplicationSummary):
    summary_type = "Material-on-application-summary"


class MaterialProductSummary(
    LoginRequiredMixin,
    NonFirearmsMaterialFlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/material/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = material_summary(self.good)
        summary = add_material_summary_edit_links(
            summary,
            MATERIAL_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
