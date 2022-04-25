import requests

from django.conf import settings
from django.http import Http404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from exporter.core.helpers import (
    get_user_organisation_documents,
    has_valid_organisation_rfd_certificate,
)
from exporter.core.services import get_organisation
from exporter.goods.services import (
    get_good,
    get_good_documents,
)


class FirearmProductDetails(LoginRequiredMixin, TemplateView):
    template_name = "goods/product-details.html"

    @cached_property
    def good_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good(self):
        return get_good(self.request, self.good_id, full_detail=True)[0]

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        try:
            organisation_id = str(self.request.session.get("organisation"))
            self.organisation = get_organisation(self.request, organisation_id)
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = get_good_documents(self.request, self.good_id)
        is_user_rfd = has_valid_organisation_rfd_certificate(self.organisation)
        organisation_documents = {
            k.replace("-", "_"): v for k, v in get_user_organisation_documents(self.organisation).items()
        }

        return {
            **context,
            "is_user_rfd": is_user_rfd,
            "good": self.good,
            "documents": documents,
            "organisation_documents": organisation_documents,
        }
