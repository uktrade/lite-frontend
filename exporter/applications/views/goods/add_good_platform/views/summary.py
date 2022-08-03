from django.views.generic import TemplateView
from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.add_good_firearm.views.mixins import (
    ApplicationMixin,
    GoodMixin,
)
from .mixins import NonFirearmsFlagMixin
from exporter.applications.summaries import (
    platform_summary,
    add_product_summary_edit_links,
    PRODUCT_SUMMARY_EDIT_LINKS,
)


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
        summary = add_product_summary_edit_links(
            summary,
            PRODUCT_SUMMARY_EDIT_LINKS,
            self.application,
            self.good,
        )
        context["summary"] = summary
        return context
