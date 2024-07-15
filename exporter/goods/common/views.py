from http import HTTPStatus

from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.summaries.summaries import get_summary_url_for_good
from exporter.goods.forms import GoodArchiveForm, GoodRestoreForm
from exporter.goods.services import archive_restore_good, get_good


class GoodArchiveRestoreBaseView(LoginRequiredMixin, FormView):
    template_name = "core/form.html"

    @property
    def good_id(self):
        return str(self.kwargs["pk"])

    def get_good_detail_url(self):
        self.good, _ = self.get_good(self.request, self.good_id)
        return get_summary_url_for_good(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = self.get_good_detail_url()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "back_link_url": self.get_good_detail_url(),
        }

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving good",
        "Unable to load product details",
    )
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def get_success_url(self):
        return self.get_good_detail_url()


class GoodArchiveView(GoodArchiveRestoreBaseView):
    form_class = GoodArchiveForm

    def form_valid(self, form):

        archive_restore_good(self.request, self.good_id, is_archived=True)

        return super().form_valid(form)


class GoodRestoreView(GoodArchiveRestoreBaseView):
    form_class = GoodRestoreForm

    def form_valid(self, form):

        archive_restore_good(self.request, self.good_id, is_archived=False)

        return super().form_valid(form)
