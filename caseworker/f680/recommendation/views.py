from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from http import HTTPStatus

from core.auth.views import LoginRequiredMixin
from core.wizard.conditionals import C
from caseworker.f680.recommendation.conditionals import (
    is_approving,
    is_refusing,
    denial_reasons_exist,
    team_provisos_exist,
)
from caseworker.f680.recommendation.constants import RecommendationSteps
from caseworker.f680.recommendation.forms.forms import (
    BasicRecommendationForm,
    BasicRecommendationRefusalReasonsForm,
    ClearRecommendationForm,
    EntityConditionsForm,
    EntityRefusalReasonsForm,
    EntitySelectionAndDecisionForm,
)
from caseworker.f680.recommendation.payloads import RecommendationPayloadBuilder
from caseworker.f680.recommendation.services import (
    clear_recommendation,
    get_case_recommendations,
    recommendations_by_current_user,
    group_recommendations_by_team_and_users,
    post_recommendation,
)
from caseworker.f680.views import F680CaseworkerMixin
from caseworker.f680.outcome.services import get_hydrated_outcomes
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView


class CaseRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/recommendation/recommendation.html"
    current_tab = "recommendations"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        case_recommendations = get_case_recommendations(self.request, self.case)
        recommendations_by_team = group_recommendations_by_team_and_users(case_recommendations)

        user_recommendations = recommendations_by_current_user(self.request, self.case, self.caseworker)
        outcomes, _ = get_hydrated_outcomes(self.request, self.case)

        return {
            **context_data,
            "case": self.case,
            "title": f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}",
            "user_recommendations": user_recommendations,
            "recommendations_by_team": recommendations_by_team,
            "pending_recommendations": list(self.pending_recommendations.values()),
            "outcomes": outcomes,
        }


class MyRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/recommendation/view_my_recommendation.html"
    current_tab = "recommendations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}"
        user_recommendations = recommendations_by_current_user(self.request, self.case, self.caseworker)

        return {
            **context,
            "title": title,
            "user_recommendations": user_recommendations,
        }


class ClearRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, FormView):
    template_name = "f680/case/recommendation/clear_recommendation.html"
    form_class = ClearRecommendationForm

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error clearing recommendation",
        "Unexpected error clearing recommendation",
    )
    def clear_recommendation(self, case):
        return clear_recommendation(self.request, case)

    def form_valid(self, form):
        self.clear_recommendation(self.case)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:f680:recommendation", kwargs=self.kwargs)


class MakeRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, BaseSessionWizardView):
    template_name = "f680/case/recommendation/form_wizard.html"
    current_tab = "recommendations"

    form_list = [
        (RecommendationSteps.ENTITIES_AND_DECISION, EntitySelectionAndDecisionForm),
        (RecommendationSteps.RELEASE_REQUEST_PROVISOS, EntityConditionsForm),
        (RecommendationSteps.RELEASE_REQUEST_NO_PROVISOS, BasicRecommendationForm),
        (RecommendationSteps.RELEASE_REQUEST_REFUSAL_REASONS, EntityRefusalReasonsForm),
        (RecommendationSteps.RELEASE_REQUEST_NO_REFUSAL_REASONS, BasicRecommendationRefusalReasonsForm),
    ]

    condition_dict = {
        RecommendationSteps.RELEASE_REQUEST_PROVISOS: C(is_approving) & C(team_provisos_exist),
        RecommendationSteps.RELEASE_REQUEST_NO_PROVISOS: C(is_approving) & ~C(team_provisos_exist),
        RecommendationSteps.RELEASE_REQUEST_REFUSAL_REASONS: C(is_refusing) & C(denial_reasons_exist),
        RecommendationSteps.RELEASE_REQUEST_NO_REFUSAL_REASONS: C(is_refusing) & ~C(denial_reasons_exist),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == RecommendationSteps.ENTITIES_AND_DECISION:
            pending_release_requests = self.pending_recommendations
            kwargs["release_requests"] = list(pending_release_requests.values())

        if step == RecommendationSteps.RELEASE_REQUEST_PROVISOS:
            kwargs["conditions"] = self.conditions

        if step == RecommendationSteps.RELEASE_REQUEST_REFUSAL_REASONS:
            kwargs["refusal_reasons"] = self.refusal_reasons
            kwargs["denial_reasons_choices"] = self.denial_reasons_choices

        return kwargs

    def get_success_url(self):
        pending_release_requests = self.pending_recommendation_requests()
        if pending_release_requests:
            return reverse("cases:f680:recommendation", kwargs=self.kwargs)

        return reverse("cases:f680:view_my_recommendation", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:f680:recommendation", kwargs=self.kwargs)
        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding recommendation",
        "Unexpected error adding recommendation",
    )
    def post_recommendation(self, data):
        return post_recommendation(self.request, self.case, data)

    def get_payload(self, form_dict):
        return RecommendationPayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        self.post_recommendation(data)
        return redirect(self.get_success_url())
