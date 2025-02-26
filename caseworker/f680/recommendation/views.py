from django.views.generic import FormView, TemplateView
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import get_case
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.f680.recommendation.forms.forms import SelectRecommendationTypeForm
from caseworker.f680.recommendation.mixins import CaseContextMixin
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


class SelectRecommendationTypeView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "f680/case/recommendation/select_recommendation_type.html"
    form_class = SelectRecommendationTypeForm

    def get_success_url(self):
        return reverse("cases:approve_all", kwargs=self.kwargs)

    def form_valid(self, form):
        self.recommendation = form.cleaned_data["recommendation"]
        return super().form_valid(form)
