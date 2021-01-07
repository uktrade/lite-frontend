import base64

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from core.auth.views import LoginRequiredMixin

from caseworker.external_data import forms, services


with open(settings.BASE_DIR + "/caseworker/external_data/example.csv", "rb") as f:
    base_64_csv = base64.b64encode(f.read()).decode()


class DenialUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "external_data/denial-upload.html"
    form_class = forms.DenialUploadForm
    success_message = "Denials created successfully"

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

    def get_context_data(self, **kwargs):
        return super().get_context_data(base_64_csv=base_64_csv, **kwargs)
