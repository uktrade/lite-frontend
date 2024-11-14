from http import HTTPStatus
from requests.exceptions import HTTPError
import rules

from caseworker.queues.services import get_queues
from caseworker.teams.services import get_all_teams
from caseworker.users.services import get_all_roles, get_gov_user, update_gov_user

from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.decorators import expect_status
from core.auth.views import LoginRequiredMixin


from .forms import EditCaseworkerUser


class EditCaseworkerUserView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = EditCaseworkerUser
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

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["teams"] = get_all_teams(self.request)
        form_kwargs["roles"] = get_all_roles(self.request)
        form_kwargs["queues"] = get_queues(self.request, include_system=True)
        form_kwargs["can_caseworker_edit_user"] = rules.test_rule("can_caseworker_edit_user", self.request)

        return form_kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        self.edit_user(data)
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
        # If user is updating their own default_queue, update the local user instance
        if str(self.user_id) == self.request.session["lite_api_user_id"]:
            self.request.session["default_queue"] = data.get("default_queue")
        return update_gov_user(self.request, self.user_id, data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context
