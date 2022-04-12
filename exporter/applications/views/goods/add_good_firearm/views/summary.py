from django.conf import settings
from django.http import Http404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application
from exporter.core.helpers import (
    get_organisation_documents,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
)
from exporter.goods.services import (
    get_good,
    get_good_documents,
)


class FirearmProductSummary(LoginRequiredMixin, TemplateView):
    template_name = "applications/goods/firearms/product-summary.html"

    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good_id(self):
        return str(self.kwargs["good_pk"])

    @cached_property
    def good(self):
        return get_good(self.request, self.good_id, full_detail=True)[0]

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = get_good_documents(self.request, self.good_id)
        application = get_application(self.request, self.application_id)
        is_user_rfd = has_valid_organisation_rfd_certificate(application)
        organisation_documents = {k.replace("-", "_"): v for k, v in get_organisation_documents(application).items()}

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "application_id": self.application_id,
            "good": self.good,
            "documents": documents,
            "organisation_documents": organisation_documents,
        }
