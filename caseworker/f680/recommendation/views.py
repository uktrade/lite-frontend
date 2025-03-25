from collections import OrderedDict

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from http import HTTPStatus

from core.auth.views import LoginRequiredMixin

from caseworker.advice.picklist_helpers import proviso_picklist
from caseworker.f680.recommendation.constants import RecommendationSteps
from caseworker.f680.recommendation.forms.forms import (
    BaseRecommendationForm,
    ClearRecommendationForm,
    EntityConditionsRecommendationForm,
)
from caseworker.f680.recommendation.payloads import RecommendationPayloadBuilder
from caseworker.f680.recommendation.services import (
    clear_recommendation,
    recommendations_by_current_user,
    get_case_recommendations,
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

        user_recommendations = recommendations_by_current_user(self.request, self.case, self.caseworker)
        recommendations_by_team = group_recommendations_by_team_and_users(case_recommendations)
        outcomes, _ = get_hydrated_outcomes(self.request, self.case)

        return {
            **context_data,
            "case": self.case,
            "title": f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}",
            "user_recommendations": user_recommendations,
            "recommendations_by_team": recommendations_by_team,
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


class BaseRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, BaseSessionWizardView):
    template_name = "f680/case/recommendation/form_wizard.html"
    current_tab = "recommendations"

    form_list = [
        (RecommendationSteps.RELEASE_REQUEST_PROVISOS, EntityConditionsRecommendationForm),
    ]

    step_kwargs = {
        RecommendationSteps.RELEASE_REQUEST_PROVISOS: proviso_picklist,
    }

    def get_success_url(self):
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


class MakeRecommendationView(BaseRecommendationView):

    def get_form_list(self):
        form_list = OrderedDict()
        for rr_key in self.security_release_requests.keys():
            form_list[rr_key] = EntityConditionsRecommendationForm

        return form_list

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        release_request = self.security_release_requests[step]
        initial = {"security_grading": release_request["security_grading"]["key"]}

        picklist_form_kwargs = self.step_kwargs[RecommendationSteps.RELEASE_REQUEST_PROVISOS](self)
        picklist_options_exist = len(picklist_form_kwargs["proviso"]["results"]) > 0
        if picklist_options_exist:
            return EntityConditionsRecommendationForm(
                initial=initial,
                prefix=step,
                data=data,
                release_request=release_request,
                **picklist_form_kwargs,
            )
        else:
            return BaseRecommendationForm(
                initial=initial,
                prefix=step,
                data=data,
                release_request=release_request,
            )
