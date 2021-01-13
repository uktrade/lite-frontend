import base64

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView

from core.auth.views import LoginRequiredMixin

from caseworker.external_data import forms, services


with open(settings.BASE_DIR + "/caseworker/external_data/example.csv", "rb") as f:
    base_64_csv = base64.b64encode(f.read()).decode()


class DenialUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "external_data/denial-upload.html"
    form_class = forms.DenialUploadForm
    success_message = "Denials created successfully"
    extra_context = {"base_64_csv": base_64_csv}

    def form_valid(self, form):
        response = services.upload_denials(request=self.request, data=form.cleaned_data)
        if not response.ok:
            for key, errors in response.json()["errors"].items():
                for error in errors:
                    form.add_error(key, error)
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()


class DenialDetailView(LoginRequiredMixin, TemplateView):
    template_name = "external_data/denial-detail.html"

    def get_context_data(self, **kwargs):
        denial = services.get_denial(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(denial=denial, **kwargs)


class DenialRevokeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "external_data/denial-revoke.html"
    success_message = "Denial successfully revoked"
    form_class = forms.DenialRevoke

    def get_context_data(self, **kwargs):
        denial = services.get_denial(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(denial=denial, **kwargs)

    def get_success_url(self):
        return reverse("external_data:denial-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        response = services.revoke_denial(
            request=self.request, pk=self.kwargs["pk"], comment=form.cleaned_data["comment"]
        )
        return super().form_valid(form)
