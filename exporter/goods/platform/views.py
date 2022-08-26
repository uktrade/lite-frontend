from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from exporter.applications.summaries.platform import platform_summary
from exporter.goods.common.mixins import ProductDetailsMixin
from exporter.applications.views.goods.add_good_platform.views.mixins import NonFirearmsPlatformFlagMixin


class PlatformProductDetails(LoginRequiredMixin, TemplateView, ProductDetailsMixin, NonFirearmsPlatformFlagMixin):
    template_name = "goods/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["good"] = self.good
        context["summary"] = platform_summary(
            self.good,
        )
        return context
