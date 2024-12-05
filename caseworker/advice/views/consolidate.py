from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse

from requests.exceptions import HTTPError

from caseworker.advice.forms.refusal import RefusalAdviceForm
from core.auth.views import LoginRequiredMixin

from caseworker.advice.forms.consolidate import (
    ConsolidateApprovalForm,
    ConsolidateSelectAdviceForm,
    LUConsolidateRefusalForm,
)
from caseworker.advice.views.views import CaseContextMixin
from caseworker.advice import services
from caseworker.core.services import get_denial_reasons, group_denial_reasons
from caseworker.picklists.services import get_picklists_list


class BaseConsolidationView(LoginRequiredMixin, CaseContextMixin, FormView):

    def get_title(self):
        return f"Review and combine case recommendation - {self.case.reference_code} - {self.case.organisation['name']}"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.team_alias = (
            self.caseworker["team"]["alias"] if self.caseworker["team"]["alias"] else self.caseworker["team"]["id"]
        )
        self.advice_to_consolidate = list(
            services.get_advice_to_consolidate(self.case.advice, self.team_alias).values()
        )

    def get_context(self, **kwargs):
        context = super().get_context()
        context["advice_to_consolidate"] = self.advice_to_consolidate
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
    form_class = ConsolidateSelectAdviceForm

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

    def get_success_url_name(self):
        if self.decision == "approve":
            return "cases:consolidate_approve"
        if self.team_alias == services.LICENSING_UNIT_TEAM:
            return "cases:consolidate_refuse_lu"
        return "cases:consolidate_refuse"

    def get_success_url(self):
        url_name = self.get_success_url_name()
        return reverse(
            url_name,
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]},
        )


class ConsolidateApproveView(BaseConsolidationView):
    """
    Consolidate advice and approve.
    """

    template_name = "advice/review_consolidate.html"
    form_class = ConsolidateApprovalForm

    def collate_all_provisos(self):
        """
        Collate all provisos across all team advice in to a single string.
        """
        # Should be a set, but dict gives us consistent ordering
        unique_provisos = {}
        for team_advice in self.advice_to_consolidate:
            for advice in team_advice:
                if advice["proviso"]:
                    unique_provisos[advice["proviso"]] = None
        return "\n\n--------\n".join(unique_provisos.keys())

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["approval_reason"] = get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
        form_kwargs["proviso"] = get_picklists_list(
            self.request, type="proviso", disable_pagination=True, show_deactivated=False
        )
        form_kwargs["initial"]["proviso"] = self.collate_all_provisos()
        return form_kwargs

    def form_valid(self, form):
        level = "final-advice" if self.team_alias == services.LICENSING_UNIT_TEAM else "team-advice"
        try:
            services.post_approval_advice(self.request, self.case, form.cleaned_data, level=level)
        except HTTPError:
            form.add_error(None, ["An error occurred when saving consolidated advice"])
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class BaseConsolidateRefuseView(BaseConsolidationView):
    """
    Base view to consolidate advice and refuse.
    """

    template_name = "advice/review_consolidate.html"
    advice_level = None

    def get_title(self):
        return f"Licence refused for case - {self.case.reference_code} - {self.case.organisation['name']}"

    def form_valid(self, form):
        try:
            data = self.build_refusal_payload(form.cleaned_data)
            services.post_refusal_advice(self.request, self.case, data, level=self.advice_level)
        except HTTPError:
            form.add_error(None, ["An error occurred when saving consolidated advice"])
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class LUConsolidateRefuseView(BaseConsolidateRefuseView):
    """
    Consolidate advice and refuse for LU.
    """

    form_class = LUConsolidateRefusalForm
    advice_level = "final-advice"

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        denial_reasons = get_denial_reasons(self.request)
        choices = group_denial_reasons(denial_reasons)
        form_kwargs["choices"] = choices
        return form_kwargs

    def build_refusal_payload(self, cleaned_data):
        data = cleaned_data
        data["text"] = data["refusal_note"]
        data["is_refusal_note"] = True
        return data


class ConsolidateRefuseView(BaseConsolidateRefuseView):
    """
    Consolidate advice and refuse for non-LU. Currently MOD-ECJU.
    """

    form_class = RefusalAdviceForm
    advice_level = "team-advice"

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        denial_reasons = get_denial_reasons(self.request)
        form_kwargs["choices"] = group_denial_reasons(denial_reasons)
        form_kwargs["refusal_reasons"] = get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
        return form_kwargs

    def build_refusal_payload(self, cleaned_data):
        data = cleaned_data
        data["text"] = data["refusal_reasons"]
        return data
