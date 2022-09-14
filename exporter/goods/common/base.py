import requests

from http import HTTPStatus

from django.http import Http404
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status_or_404

from exporter.core.services import get_organisation
from exporter.goods.services import get_good


class BaseProductDetails(LoginRequiredMixin, TemplateView):
    template_name = "goods/product-details.html"

    @expect_status_or_404(HTTPStatus.OK)
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def dispatch(self, request, *args, **kwargs):
        organisation_id = str(self.request.session.get("organisation"))
        try:
            self.organisation = get_organisation(self.request, organisation_id)
        except requests.exceptions.HTTPError:
            raise Http404

        good_id = str(self.kwargs["pk"])
        try:
            self.good, _ = self.get_good(self.request, good_id)
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_summary(self):
        raise NotImplementedError(f"Implement `get_summary` on {self.__class__.__name__}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good
        context["summary"] = self.get_summary()

        return context
