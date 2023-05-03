from http import HTTPStatus

from django.contrib import messages
from django.views.generic import FormView

from caseworker.bookmarks import forms
from core import client
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from caseworker.users.services import get_gov_user


# Create your views here.
class AddBookmark(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.AddBookmark

    def form_valid(self, form):
        user, _ = get_gov_user(self.request)
        data = form.cleaned_data
        return_to = data["return_to"]
        self.add_bookmark(user["user"]["id"], **data)
        messages.success(self.request, f"Bookmark saved")
        self.success_url = return_to

        return super().form_valid(form)

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding bookmark",
        "Unexpected error adding bookmark",
    )
    def add_bookmark(self, user_id, return_to, name, description):
        data = {"url": return_to, "name": name, "description": description, "user_id": user_id}
        response = client.post(self.request, f"/cases/bookmarks", data)
        return response.json(), response.status_code


class DeleteBookmark(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.DeleteBookmark

    def form_valid(self, form):
        user, _ = get_gov_user(self.request)
        data = form.cleaned_data
        url = data["url"]
        return_to = data["return_to"]

        self.delete_bookmark(user["user"]["id"], url)
        messages.success(self.request, f"Bookmark deleted")
        self.success_url = return_to

        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error deleting bookmark",
        "Unexpected error deleting bookmark",
    )
    def delete_bookmark(self, user_id, url):
        data = {"user_id": user_id, "url": url}
        response = client.delete(self.request, f"/cases/bookmarks", data)
        return response.json(), response.status_code
