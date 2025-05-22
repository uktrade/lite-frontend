from collections import defaultdict
from datetime import date, datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView

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


class Finalise(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Finalise a case and change the case status to finalised
    """

    template_name = "case/finalise.html"
    formset_class = GoodQuantityValueForm

    def get_initial(self):
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

    def get_form(self):
        licence_data, _ = get_licence(self.request, str(self.case.id))
        self.licence = licence_data.get("licence")
        form_kwargs = self.get_form_kwargs()
        final_advice = filter_advice_by_level(self.case["advice"], "final")
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
        form_kwargs["editable_duration"] = helpers.has_permission(self.request, Permission.MANAGE_LICENCE_DURATION)

        if case_data["approve"]:
            if self.licence:
                return ReissueLicenceForm(**form_kwargs)
            else:
                return ApproveLicenceForm(**form_kwargs)
        else:
            return DenyLicenceForm(**form_kwargs)

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context["goods"] = self.case.goods
        context["formset"] = get_formset(self.formset_class, len(self.case.goods), initial=self.case.goods)
        return context

    def format_formset_data(self, goods, formset_data):
        data = {}
        for index, good in enumerate(goods):
            # given an api change this could/should look like:
            # {"<ID>":{"quantity":x,"value":y}}
            data[f'quantity-{good["id"]}'] = good["id"]
            data[f'value-{good["id"]}'] = formset_data[index]["value"]
        return data

    def form_valid(self, form):
        context = self.get_context()
        goods = context["goods"]
        formset = get_formset(self.formset_class, len(goods), data=self.request.POST)

        if formset.is_valid():
            # format data to be sent and send
            data = {
                "case_type": form.cleaned_data["case_type"],
                "duration": form.cleaned_data["duration"],
                "day": form.cleaned_data["date"].day,
                "month": form.cleaned_data["date"].month,
                "year": form.cleaned_data["date"].year,
            }
            data.update(self.format_formset_data(goods, formset.cleaned_data))

            finalise_application(self.request, self.case.id, data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:finalise_documents", kwargs=self.kwargs)


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
