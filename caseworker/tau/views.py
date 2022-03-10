from django.views.generic import TemplateView

from caseworker.cases.services import get_case
from core.auth.views import LoginRequiredMixin


class TAUHome(LoginRequiredMixin, TemplateView):
    """This renders a placeholder home page for TAU 2.0."""

    template_name = "tau/home.html"

    def get_context_data(self, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(self.request, case_id)
        return {"case": case, "greetings": f"Welcome to TAU 2.0! Case: {case.id}"}
