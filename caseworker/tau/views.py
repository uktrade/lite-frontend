from django.views.generic import TemplateView
from django.utils.functional import cached_property

from caseworker.cases.services import get_case
from core.auth.views import LoginRequiredMixin


class TAUHome(LoginRequiredMixin, TemplateView):
    """This renders a placeholder home page for TAU 2.0."""

    template_name = "tau/home.html"

    @cached_property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = self.case
        return {**context, "case": case, "greetings": f"Welcome to TAU 2.0! Case: {case.id}"}
