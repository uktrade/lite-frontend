from http import HTTPStatus

from django.http import Http404
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.summaries.summaries import get_summary_type_for_good

from exporter.core.services import get_organisation
from exporter.goods.constants import GoodStatus
from exporter.goods.services import get_good


class BaseProductDetails(LoginRequiredMixin, TemplateView):
    template_name = "goods/product-details.html"
    summary_type = None

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving good",
        "Unable to load product details",
    )
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def dispatch(self, request, *args, **kwargs):
        if not self.summary_type:
            raise ValueError(f"No summary type specified for {self.__class__.__name__}")

        organisation_id = str(self.request.session.get("organisation"))
        self.organisation = get_organisation(self.request, organisation_id)

        good_id = str(self.kwargs["pk"])
        self.good, _ = self.get_good(self.request, good_id)

        summary_type = get_summary_type_for_good(self.good)
        if summary_type != self.summary_type:
            raise Http404(f"Incorrect summary type {summary_type} should be {self.summary_type}")

        return super().dispatch(request, *args, **kwargs)

    def get_summary(self):
        raise NotImplementedError(f"Implement `get_summary` on {self.__class__.__name__}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good
        context["summary"] = self.get_summary()
        context["allow_delete"] = self.good["status"]["key"] == GoodStatus.DRAFT
        context["allow_archive"] = (
            self.good["status"]["key"] in [GoodStatus.SUBMITTED, GoodStatus.VERIFIED]
            or self.good["is_archived"] is False
        )
        context["allow_restore"] = self.good["is_archived"] is True
        context["archive_button_text"] = "Archive product" if context["allow_archive"] else "Restore product"

        return context
