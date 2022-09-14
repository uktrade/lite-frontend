from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.summaries.component import component_summary
from exporter.goods.common.mixins import ProductDetailsMixin


class ComponentProductDetails(LoginRequiredMixin, ProductDetailsMixin, TemplateView):
    template_name = "goods/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good
        context["summary"] = component_summary(self.good)

        return context
