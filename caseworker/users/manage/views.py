from requests.exceptions import HTTPError
from http import HTTPStatus
import rules

from django.http import Http404, HttpResponseForbidden
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.decorators import expect_status
from core.auth.views import LoginRequiredMixin
from caseworker.queues.services import get_queues
from caseworker.teams.services import get_all_teams
from .forms import EditCaseworkerQueue, EditCaseworker, AddCaseworkerUser
from caseworker.users.services import get_all_roles, get_gov_user, post_gov_users, update_gov_user


class EditCaseworkerUserView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = EditCaseworkerQueue

    template_name = "core/form.html"
    success_message = "User updated successfully"

    def dispatch(self, *args, **kwargs):
        try:
            self.user_id = kwargs["pk"]
            self.user, _ = get_gov_user(self.request, self.user_id)
            self.user = self.user["user"]
        except HTTPError:
            raise Http404()

        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        return {
            "email": self.user["email"],
            "role": self.user["role"]["id"],
            "team": self.user["team"]["id"],
            "default_queue": self.user["default_queue"]["id"],
        }

    def get_form_class(self):
        if rules.test_rule("can_caseworker_edit_user", self.request):
            return EditCaseworker
        return EditCaseworkerQueue

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["teams"] = get_all_teams(self.request)
        form_kwargs["roles"] = get_all_roles(self.request)
        form_kwargs["queues"] = get_queues(self.request, include_system=True)

        return form_kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        self.edit_user(data)
        # If user is updating their own default_queue, update the local user instance
        if str(self.user_id) == self.request.session["lite_api_user_id"]:
            self.request.session["default_queue"] = data.get("default_queue")
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy("users:user", kwargs={"pk": self.user_id})
        return self.success_url

    @expect_status(
        HTTPStatus.OK,
        "Error editing user",
        "Unexpected error editing user",
    )
    def edit_user(self, data):
        return update_gov_user(self.request, self.user_id, data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context


class AddCaseworkerUserView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AddCaseworkerUser
    template_name = "core/form.html"
    success_message = "User added successfully"

    def dispatch(self, *args, **kwargs):
        if not rules.test_rule("can_caseworker_add_user", self.request):
            return HttpResponseForbidden()
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["teams"] = get_all_teams(self.request)
        form_kwargs["roles"] = get_all_roles(self.request)
        form_kwargs["queues"] = get_queues(self.request, include_system=True)
        return form_kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        self.add_user(data)
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy("users:users")
        return self.success_url

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding user",
        "Unexpected error adding user",
    )
    def add_user(self, data):
        return post_gov_users(self.request, data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context
