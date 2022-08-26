from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from exporter.applications.summaries.material import material_summary
from exporter.goods.common.mixins import ProductDetailsMixin
from exporter.applications.views.goods.add_good_material.views.mixins import NonFirearmsMaterialFlagMixin


class MaterialProductDetails(LoginRequiredMixin, TemplateView, ProductDetailsMixin, NonFirearmsMaterialFlagMixin):
    template_name = "goods/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["good"] = self.good
        context["summary"] = material_summary(
            self.good,
        )
        return context
