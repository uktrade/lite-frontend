from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import get_case
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.queues.services import get_queue


class CaseRecommendationView(LoginRequiredMixin, CaseworkerMixin, TemplateView):
    template_name = "f680/case/recommendation/recommendation.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        return context_data

