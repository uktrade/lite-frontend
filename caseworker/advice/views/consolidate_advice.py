from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from caseworker.advice import forms
from caseworker.advice.views.views import CaseContextMixin
from caseworker.advice import services


class BaseConsolidationView(LoginRequiredMixin, CaseContextMixin, FormView):

    def get_title(self):
        return f"Review and combine case recommendation - {self.case.reference_code} - {self.case.organisation['name']}"

    def get_context(self, **kwargs):
        context = super().get_context()
        team_alias = (
            self.caseworker["team"]["alias"] if self.caseworker["team"]["alias"] else self.caseworker["team"]["id"]
        )
        advice_to_consolidate = services.get_advice_to_consolidate(self.case.advice, team_alias)
        context["advice_to_consolidate"] = list(advice_to_consolidate.values())
        context["denial_reasons_display"] = self.denial_reasons_display
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        context["title"] = self.get_title()
        return context


class ConsolidateSelectDecisionView(BaseConsolidationView):
    """
    Initial selection of consolidated decision between approve and refuse.
    This will redirect to the consolidate approval or consolidate refusal flows as appropriate.
    """

    template_name = "advice/review_consolidate.html"
    form_class = forms.ConsolidateSelectAdviceForm

    def dispatch(self, request, *args, **kwargs):
        approve_advice_types = ("approve", "proviso", "no_licence_required")
        is_all_advice_approval = all(a["type"]["key"] in approve_advice_types for a in self.case.advice)
        if is_all_advice_approval:
            self.decision = "approve"
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        team_name = self.caseworker["team"]["name"]
        form_kwargs.update({"team_name": team_name})
        return form_kwargs

    def form_valid(self, form):
        self.decision = form.cleaned_data["recommendation"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "cases:consolidate",
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "advice_type": self.decision},
        )
