from http import HTTPStatus
from requests.exceptions import HTTPError
from caseworker.users.services import put_gov_user

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
            self.user, _ = get_gov_user(request, self.object_pk)
        except HTTPError:
            raise Http404()

        # if not rules.test_rule("can_user_manage_organisation", self.request, self.organisation):
        #    raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        # users = get_organisation_members(self.request, self.organisation_id)
        # organisation_users = set(user["email"] for user in users)
        return form_kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        # This is currently limited to Administrator
        # data["role"] = ExporterRoles.administrator.id
        self.edit_user(data)
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy("users:user", kwargs={"pk": self.user_id})
        return self.success_url

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding user to organisation",
        "Unexpected error adding user to organisation",
    )
    def edit_user(self, data):
        pass
        # If user is updating their own default_queue, update the local user instance
        # if self.user_id == self.request.session["lite_api_user_id"]:
        #    self.request.session["default_queue"] = self.get_validated_data().get("gov_user").get("default_queue")
        return put_gov_user(self.request, self.user_id, data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context
