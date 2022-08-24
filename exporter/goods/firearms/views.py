from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from exporter.applications.summaries.firearm import firearm_summary
from exporter.core.helpers import (
    get_user_organisation_documents,
    has_valid_organisation_rfd_certificate,
)
from exporter.goods.common.mixins import ProductDetailsMixin

from exporter.applications.views.goods.add_good_firearm.views.mixins import Product2FlagMixin


class FirearmProductDetails(LoginRequiredMixin, Product2FlagMixin, ProductDetailsMixin, TemplateView):
    template_name = "goods/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good

        is_user_rfd = has_valid_organisation_rfd_certificate(self.organisation)
        organisation_documents = get_user_organisation_documents(self.organisation)
        context["summary"] = firearm_summary(
            self.good,
            is_user_rfd,
            organisation_documents,
        )

        return context
