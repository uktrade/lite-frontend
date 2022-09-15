from http import HTTPStatus

from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.core.services import get_organisation
from exporter.goods.services import get_good


class BaseProductDetails(LoginRequiredMixin, TemplateView):
    template_name = "goods/product-details.html"

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving good",
        "Unable to load product details",
    )
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def dispatch(self, request, *args, **kwargs):
        organisation_id = str(self.request.session.get("organisation"))
        self.organisation = get_organisation(self.request, organisation_id)

        good_id = str(self.kwargs["pk"])
        self.good, _ = self.get_good(self.request, good_id)

        return super().dispatch(request, *args, **kwargs)

    def get_summary(self):
        raise NotImplementedError(f"Implement `get_summary` on {self.__class__.__name__}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good
        context["summary"] = self.get_summary()

        return context
