from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.summaries.f680 import (
    f680_good_details_summary,
    f680_good_details_on_application_summary,
)
from exporter.core.helpers import get_organisation_documents


class BaseF680GoodDetailsApplicationSummary(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    TemplateView,
):
    template_name = "applications/goods/f680/product-on-application-summary.html"

    @cached_property
    def organisation_documents(self):
        return get_organisation_documents(self.application)

    def get_f680_good_details_summary(self):
        product_summary = f680_good_details_summary(
            self.good,
        )
        return product_summary

    def get_f680_good_details_on_application_summary(self):
        product_on_application_summary = f680_good_details_on_application_summary(
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
            "product_summary": self.get_f680_good_details_summary(),
            "product_on_application_summary": self.get_f680_good_details_on_application_summary(),
        }


class CompleteF680GoodDetailsOnApplicationSummary(BaseF680GoodDetailsApplicationSummary):
    summary_type = "f680_good_details-on-application-summary"


class CompleteF680GoodDetailsSummary(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/f680/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = self.application["id"]
        context["good"] = self.good

        summary = f680_good_details_summary(self.good)

        context["summary"] = summary
        return context
