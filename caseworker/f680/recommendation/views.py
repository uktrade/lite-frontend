from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from http import HTTPStatus

from core.auth.views import LoginRequiredMixin

from caseworker.advice.constants import AdviceLevel, AdviceSteps
from caseworker.advice.conditionals import form_add_licence_conditions
from caseworker.advice.payloads import GiveApprovalAdvicePayloadBuilder
from caseworker.advice.picklist_helpers import approval_picklist, footnote_picklist, proviso_picklist
from caseworker.f680.recommendation.forms.forms import (
    FootnotesApprovalAdviceForm,
    PicklistLicenceConditionsForm,
    RecommendAnApprovalForm,
    SelectRecommendationTypeForm,
    SimpleLicenceConditionsForm,
)
from caseworker.f680.recommendation.services import (
    current_user_recommendation,
    post_approval_recommendation,
)
from caseworker.f680.views import F680CaseworkerMixin
from core.decorators import expect_status
from core.wizard.conditionals import C
from core.wizard.views import BaseSessionWizardView


class CaseRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/recommendation/recommendation.html"
    current_tab = "recommendations"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        recommendation = None
        if user_recommendation := current_user_recommendation(
            self.case.advice, self.caseworker, self.recommendation_level
        ):
            user_recommendation = user_recommendation[0] if user_recommendation else None

        team_recommendations = []
        for recommendation in self.case.get("advice", []):
            team_recommendations.append({"team": recommendation["team"], "recommendation": recommendation})
        return {
            **context_data,
            "case": self.case,
            "title": f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}",
            "user_recommendation": user_recommendation,
            "teams_recommendations": team_recommendations,
        }


class MyRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/recommendation/view_my_recommendation.html"
    current_tab = "recommendations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}"
        recommendation = current_user_recommendation(self.case.advice, self.caseworker, self.recommendation_level)

        return {
            **context,
            "title": title,
            "recommendation": recommendation[0] if recommendation else None,
        }


class SelectRecommendationTypeView(LoginRequiredMixin, F680CaseworkerMixin, FormView):
    template_name = "f680/case/recommendation/select_recommendation_type.html"
    form_class = SelectRecommendationTypeForm
    current_tab = "recommendations"

    def get_success_url(self):
        return reverse("cases:f680:approve_all", kwargs=self.kwargs)

    def form_valid(self, form):
        self.recommendation = form.cleaned_data["recommendation"]
        return super().form_valid(form)


class BaseApprovalRecommendationView(LoginRequiredMixin, F680CaseworkerMixin, BaseSessionWizardView):
    template_name = "f680/case/recommendation/form_wizard.html"
    current_tab = "recommendations"

    condition_dict = {
        AdviceSteps.LICENCE_CONDITIONS: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
        AdviceSteps.LICENCE_FOOTNOTES: C(form_add_licence_conditions(AdviceSteps.RECOMMEND_APPROVAL)),
    }

    form_list = [
        (AdviceSteps.RECOMMEND_APPROVAL, RecommendAnApprovalForm),
        (AdviceSteps.LICENCE_CONDITIONS, PicklistLicenceConditionsForm),
        (AdviceSteps.LICENCE_FOOTNOTES, FootnotesApprovalAdviceForm),
    ]

    step_kwargs = {
        AdviceSteps.RECOMMEND_APPROVAL: approval_picklist,
        AdviceSteps.LICENCE_CONDITIONS: proviso_picklist,
        AdviceSteps.LICENCE_FOOTNOTES: footnote_picklist,
    }

    def get_success_url(self):
        return reverse("cases:f680:view_my_recommendation", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("cases:f680:select_recommendation_type", kwargs=self.kwargs)
        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding approval recommendation",
        "Unexpected error adding approval recommendation",
    )
    def post_approval_recommendation(self, data):
        level = "final-advice" if self.recommendation_level == AdviceLevel.FINAL else "user-advice"
        return post_approval_recommendation(self.request, self.case, data, level=level)

    def get_payload(self, form_dict):
        return GiveApprovalAdvicePayloadBuilder().build(form_dict)

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        self.post_approval_recommendation(data)
        return redirect(self.get_success_url())


class GiveApprovalRecommendationView(BaseApprovalRecommendationView):

    def get_form(self, step=None, data=None, files=None):

        if step == AdviceSteps.LICENCE_CONDITIONS:
            picklist_form_kwargs = self.step_kwargs[AdviceSteps.LICENCE_CONDITIONS](self)
            picklist_options_exist = len(picklist_form_kwargs["proviso"]["results"]) > 0
            if picklist_options_exist:
                return PicklistLicenceConditionsForm(data=data, prefix=step, **picklist_form_kwargs)
            else:
                return SimpleLicenceConditionsForm(data=data, prefix=step)

        return super().get_form(step, data, files)
