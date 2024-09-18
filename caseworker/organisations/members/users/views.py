from http import HTTPStatus
from requests.exceptions import HTTPError
import rules

from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.constants import ExporterRoles
from core.decorators import expect_status
from core.auth.views import LoginRequiredMixin

from caseworker.organisations.members.services import create_exporter_user
from caseworker.organisations.services import get_organisation, get_organisation_members, get_organisation_sites

from .forms import AddAdminExporterUserForm


class AddExporterAdminView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AddAdminExporterUserForm
    template_name = "core/form.html"
    success_message = "Administrator successfully added to organisation"

    def dispatch(self, *args, **kwargs):
        try:
            self.organisation_id = kwargs["pk"]
            self.organisation = get_organisation(self.request, self.organisation_id)
        except HTTPError:
            raise Http404()

        if not rules.test_rule("can_user_manage_organisation", self.request, self.organisation):
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        users = get_organisation_members(self.request, self.organisation_id)
        organisation_users = set(user["email"] for user in users)
        form_kwargs["cancel_url"] = self.get_success_url()
        form_kwargs["organisation_users"] = organisation_users
        form_kwargs["sites"] = get_organisation_sites(self.request, self.organisation_id)
        return form_kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        # This is currently limited to Administrator
        data["role"] = ExporterRoles.administrator.id
        self.post_add_user(data)
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy("organisations:organisation_members", kwargs={"pk": self.organisation_id})
        return self.success_url

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding user to organisation",
        "Unexpected error adding user to organisation",
    )
    def post_add_user(self, data):
        return create_exporter_user(self.request, self.organisation_id, data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context
