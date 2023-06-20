from http import HTTPStatus

from django.contrib import messages
from django.utils.functional import cached_property
from django.views.generic import FormView

from caseworker.bookmarks import forms, services
from caseworker.core.services import get_control_list_entries
from caseworker.flags.services import get_flags
from caseworker.queues.views.cases import CaseDataMixin
from caseworker.queues.views.forms import CasesFiltersForm
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class AddBookmark(LoginRequiredMixin, CaseDataMixin, FormView):
    template_name = "core/form.html"
    form_class = CasesFiltersForm

    @cached_property
    def all_cles(self):
        return get_control_list_entries(self.request, include_parent=True)

    def form_valid(self, form):
        data = form.cleaned_data
        self.add_bookmark(data)
        messages.success(self.request, f"Bookmark saved")
        self.success_url = data["return_to"]

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["filters_data"] = self.filters
        kwargs["all_flags"] = get_flags(self.request, disable_pagination=True)
        kwargs["all_cles"] = self.all_cles
        kwargs["queue"] = self.queue
        kwargs["all_flags"] = get_flags(self.request, disable_pagination=True)

        return kwargs

    @expect_status(
        HTTPStatus.CREATED,
        "Error saving filter",
        "Unexpected error saving filter",
    )
    def add_bookmark(self, data):
        response = services.add_bookmark(self.request, data, self.request.POST)
        return response.json(), response.status_code


class DeleteBookmark(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.DeleteBookmark

    def form_valid(self, form):
        data = form.cleaned_data
        bookmark_id = data["id"]
        return_to = data["return_to"]

        self.delete_bookmark(bookmark_id)

        messages.success(self.request, f"Saved filter deleted")
        self.success_url = return_to

        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error deleting filter",
        "Unexpected error deleting filter",
    )
    def delete_bookmark(self, bookmark_id):
        response = services.delete_bookmark(self.request, bookmark_id)
        return response.json(), response.status_code


class RenameBookmark(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.RenameBookmark

    def form_valid(self, form):
        data = form.cleaned_data
        bookmark_id = data["id"]
        return_to = data["return_to"]

        self.rename_bookmark(bookmark_id, data["name"])

        messages.success(self.request, f"Saved filter renamed")
        self.success_url = return_to

        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error editing filter name",
        "Unexpected error editing filter name",
    )
    def rename_bookmark(self, bookmark_id, name):
        response = services.rename_bookmark(self.request, bookmark_id, name)
        return response.json(), response.status_code
