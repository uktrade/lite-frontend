from django.urls import reverse
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin

from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.payloads import get_cleaned_data
from exporter.goods.forms.common import ProductNameForm
from exporter.goods.services import edit_platform

from .mixins import NonFirearmsFlagMixin


class BaseEditView(
    LoginRequiredMixin,
    NonFirearmsFlagMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        return reverse("applications:platform_summary", kwargs=self.kwargs)

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def form_valid(self, form):
        edit_platform(self.request, self.good["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = reverse("applications:platform_summary", kwargs=self.kwargs)

        return ctx


class BasePlatformEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class PlatformEditName(BasePlatformEditView):
    form_class = ProductNameForm

    def get_initial(self):
        return {"name": self.good["name"]}
