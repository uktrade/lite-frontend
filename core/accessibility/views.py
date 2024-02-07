from django.views.generic import TemplateView
from django.urls import reverse

from core.auth.views import LoginRequiredMixin


class BaseAccessibilityStatementView(LoginRequiredMixin, TemplateView):
    template_name = "accessibility/accessibility.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        protocol = "https://" if self.request.is_secure() else "http://"
        context["host"] = f"{protocol}{self.request.get_host()}/"
        return context


class ExporterAccessibilityStatementView(BaseAccessibilityStatementView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = reverse("core:home")
        return context


class CaseworkerAccessibilityStatementView(BaseAccessibilityStatementView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = reverse("core:index")

        return context
