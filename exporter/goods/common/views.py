from http import HTTPStatus

from django.shortcuts import redirect
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.summaries.summaries import get_summary_url_for_good
from exporter.goods.forms import GoodArchiveForm, GoodRestoreForm
from exporter.goods.services import get_good, edit_good


class GoodArchiveRestoreView(LoginRequiredMixin, FormView):
    template_name = "core/form.html"

    def get_good_detail_url(self):
        good_id = str(self.kwargs["pk"])
        self.good, _ = self.get_good(self.request, good_id)
        return get_summary_url_for_good(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = self.get_good_detail_url()
        return kwargs

    def is_archiving(self):
        return self.kwargs["action"] == "archive"

    def get_form(self):
        if self.is_archiving():
            return GoodArchiveForm(**self.get_form_kwargs())
        else:
            return GoodRestoreForm(**self.get_form_kwargs())

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving good",
        "Unable to load product details",
    )
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def get_success_url(self):
        return self.get_good_detail_url()

    def form_valid(self, form):
        post_keys = self.request.POST.keys()

        if "cancel" in post_keys:
            return redirect(self.get_good_detail_url())

        good_id = str(self.kwargs["pk"])
        data = {"is_archived": self.is_archiving()}

        edit_good(self.request, good_id, data)

        return super().form_valid(form)
