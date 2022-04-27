from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application
from exporter.core.helpers import (
    get_organisation_documents,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from exporter.goods.services import get_good_documents
from .mixins import (
    ApplicationMixin,
    GoodMixin,
    Product2FlagMixin,
)


class FirearmProductSummary(
    LoginRequiredMixin,
    Product2FlagMixin,
    ApplicationMixin,
    GoodMixin,
    TemplateView,
):
    template_name = "applications/goods/firearms/product-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = get_good_documents(self.request, self.good["id"])
        application = get_application(self.request, self.application["id"])
        is_user_rfd = has_valid_organisation_rfd_certificate(application)
        organisation_documents = {k.replace("-", "_"): v for k, v in get_organisation_documents(application).items()}

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "application_id": self.application["id"],
            "good": self.good,
            "documents": documents,
            "organisation_documents": organisation_documents,
        }
