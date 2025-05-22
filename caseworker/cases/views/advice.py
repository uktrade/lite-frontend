from collections import defaultdict
from datetime import date, datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from caseworker.advice.views.mixins import CaseContextMixin
from caseworker.cases.forms.advice import (
    finalise_goods_countries_form,
    generate_documents_form,
)
from caseworker.cases.forms.finalise_case import (
    ApproveLicenceForm,
    DenyLicenceForm,
    GoodQuantityValueForm,
    ReissueLicenceForm,
    get_formset,
)
from caseworker.cases.services import (
    coalesce_user_advice,
    coalesce_team_advice,
    clear_team_advice,
    clear_final_advice,
    get_application_default_duration,
    get_case,
    finalise_application,
    get_good_countries_decisions,
    grant_licence,
    get_final_decision_documents,
    get_licence,
    post_good_countries_decisions,
)
from caseworker.core import helpers
from caseworker.core.constants import Permission
from core.builtins.custom_tags import filter_advice_by_level
from lite_content.lite_internal_frontend.advice import GenerateGoodsDecisionForm
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class CoalesceUserAdvice(LoginRequiredMixin, TemplateView):
    """
    Group all of a user's team's user level advice in a team advice for the user's team
    """

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_user_advice(request, case_id)
        messages.success(self.request, "User advice combined successfully")
        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "team-advice"})
            + "?grouped-advice-view="
            + request.GET.get("grouped-advice-view", "")
        )


class ClearTeamAdvice(LoginRequiredMixin, TemplateView):
    """
    Clear the user's team's team level advice
    """

    def post(self, request, **kwargs):
        case = get_case(request, kwargs["pk"])

        if request.POST.get("action") == "delete":
            clear_team_advice(request, case.get("id"))

            messages.success(self.request, "Team advice cleared successfully")

            return redirect(
                reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "team-advice"})
                + "?grouped-advice-view="
                + request.GET.get("grouped-advice-view", "")
            )


class CoalesceTeamAdvice(LoginRequiredMixin, TemplateView):
    """
    Group all team's advice into final advice
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_team_advice(request, case_id)
        messages.success(self.request, "Team advice combined successfully")
        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "final-advice"})
            + "?grouped-advice-view="
            + request.GET.get("grouped-advice-view", "")
        )


class ClearFinalAdvice(LoginRequiredMixin, TemplateView):
    """
    Clear final advice
    """

    def post(self, request, **kwargs):
        case = get_case(request, kwargs["pk"])

        if request.POST.get("action") == "delete":
            clear_final_advice(request, case.get("id"))

        messages.success(self.request, "Final advice cleared successfully")

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "final-advice"})
            + "?grouped-advice-view="
            + request.GET.get("grouped-advice-view", "")
        )


def create_mapping(goods):
    return_dict = defaultdict(list)

    for good in goods:
        for country in good["countries"]:
            return_dict[good].append(country)

    return return_dict


class FinaliseGoodsCountries(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.context = {
            "case": get_case(request, self.object_pk),
            "goods_type_country_decisions": get_good_countries_decisions(request, self.object_pk),
            "decisions": {"approve": "Approve", "refuse": "Reject"},
        }
        self.form = finalise_goods_countries_form(kwargs["pk"], kwargs["queue_pk"])
        self.action = post_good_countries_decisions
        self.success_url = reverse_lazy("cases:finalise", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})


class Finalise(LoginRequiredMixin, CaseContextMixin, TemplateView):
    """
    Finalise a case and change the case status to finalised
    """

    template_name = "case/finalise.html"

    form_class = ApproveLicenceForm
    formset_class = GoodQuantityValueForm

    def get_initial_data(self):
        if self.licence:
            start_date = datetime.strptime(self.licence["start_date"], "%Y-%m-%d")
            duration = self.licence["duration"]
        else:
            start_date = date.today()
            duration = get_application_default_duration(self.request, str(self.case.id))

        return {
            "date": start_date,
            "duration": duration,
        }

    def get_context(self, **kwargs):
        context = super().get_context()
        final_advice = filter_advice_by_level(self.case["advice"], "final")
        licence_data, _ = get_licence(self.request, str(self.case.id))
        self.licence = licence_data.get("licence")
        data = {}
        # For no licence required advice items we have recorded their decision as ‘approve’
        # but their ‘good_id’ has been set to ‘None’ so it is best to filter out
        # these advice items.

        advice_items_with_goods = [item["type"]["key"] for item in final_advice if item["good"]]

        # Reuse advice has no good associated with it so we need to find tout if there is
        # any on the application to decide whether to use the refuse or nlr flow

        case_data = {
            "refuse_advice": any([item["type"]["key"] == "refuse" for item in final_advice]),
            "approve": any([item == "approve" or item == "proviso" for item in advice_items_with_goods]),
            "any_nlr": any([item == "no_licence_required" for item in advice_items_with_goods]),
            "all_nlr": all(item == "no_licence_required" for item in advice_items_with_goods),
            "has_proviso": any([item == "proviso" for item in advice_items_with_goods]),
        }
        data["editable_duration"] = helpers.has_permission(self.request, Permission.MANAGE_LICENCE_DURATION)

        if case_data["approve"]:
            data["initial"] = self.get_initial_data()
            # If there are licenced goods, we want to use the reissue goods flow.
            if self.licence:
                self.form_class = ReissueLicenceForm
            else:
                self.form_class = ApproveLicenceForm
        else:
            self.form_class = DenyLicenceForm

        context["form"] = self.form_class(**data)
        context["goods"] = self.case.goods
        context["formset"] = get_formset(self.formset_class, len(self.case.goods), initial=self.case.goods)
        context["title"] = f"{self.form_class.DOCUMENT_TITLE}"
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        goods = context["goods"]
        formset = get_formset(self.formset_class, len(goods), data=request.POST)
        form = self.form_class(data=request.POST)

        if formset.is_valid() and form.is_valid():
            # format data to be sent and send

            res = finalise_application(request, self.case.id, formset.cleaned_data)

        return redirect(
            reverse_lazy(
                "cases:finalise_documents",
                kwargs=kwargs,
            )
        )


class FinaliseGenerateDocuments(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = generate_documents_form(kwargs["queue_pk"], self.object_pk)
        decisions, _ = get_final_decision_documents(request, self.object_pk)

        # Remove the inform letter from finalisation documents

        decisions = {key: value for (key, value) in decisions["documents"].items() if key != "inform"}
        can_submit = all([decision.get("document") for decision in decisions.values()])
        self.context = {
            "case": case,
            "can_submit": can_submit,
            "decisions": decisions,
        }
        self.action = grant_licence
        self.success_message = GenerateGoodsDecisionForm.SUCCESS_MESSAGE
        self.success_url = reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})
