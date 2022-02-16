from collections import defaultdict
from http import HTTPStatus

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from caseworker.cases.constants import CaseType
from caseworker.cases.forms.advice import (
    give_advice_form,
    finalise_goods_countries_form,
    generate_documents_form,
    reissue_finalise_form,
    finalise_form,
)
from caseworker.cases.forms.finalise_case import deny_licence_form
from caseworker.cases.helpers.advice import (
    get_param_destinations,
    get_param_goods,
    flatten_advice_data,
    prepare_data_for_advice,
)
from caseworker.cases.services import (
    post_user_case_advice,
    coalesce_user_advice,
    coalesce_team_advice,
    post_team_case_advice,
    post_final_case_advice,
    clear_team_advice,
    clear_final_advice,
    get_case,
    finalise_application,
    get_good_countries_decisions,
    grant_licence,
    get_final_decision_documents,
    get_licence,
    get_finalise_application_goods,
    post_good_countries_decisions,
    get_open_licence_decision,
)
from core.builtins.custom_tags import filter_advice_by_level
from caseworker.core.services import get_denial_reasons
from lite_content.lite_internal_frontend.advice import FinaliseLicenceForm, GenerateGoodsDecisionForm
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class GiveAdvice(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.case = get_case(request, self.object_pk)
        self.tab = kwargs["tab"]
        self.data = flatten_advice_data(
            request,
            self.case,
            [*get_param_goods(request, self.case), *get_param_destinations(request, self.case)],
            self.tab,
        )
        self.form = give_advice_form(
            request,
            self.case,
            self.tab,
            kwargs["queue_pk"],
            get_denial_reasons(request, True, True),
        )
        self.context = {
            "case": self.case,
            "goods": get_param_goods(request, self.case),
            "destinations": get_param_destinations(request, self.case),
        }
        self.success_message = "Advice posted successfully"
        self.success_url = (
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": self.tab})
            + "?grouped-advice-view="
            + request.GET.get("grouped-advice-view", "")
        )

        if self.tab not in ["user-advice", "team-advice", "final-advice"]:
            raise Http404

    def clean_data(self, data):
        data["good"] = self.request.GET.getlist("goods")
        data["goods_type"] = self.request.GET.getlist("goods_types")
        data["country"] = self.request.GET.getlist("countries")
        data["third_party"] = self.request.GET.getlist("third_party")
        data["ultimate_end_user"] = self.request.GET.getlist("ultimate_end_user")
        data["third_party"] = self.request.GET.getlist("third_party")
        data["consignee"] = self.request.GET.get("consignee")
        data["end_user"] = self.request.GET.get("end_user")
        data["denial_reasons"] = self.request.POST.getlist("denial_reasons[]", [])

        return prepare_data_for_advice(data)

    def get_action(self):
        if self.tab == "user-advice":
            return post_user_case_advice
        elif self.tab == "team-advice":
            return post_team_case_advice
        elif self.tab == "final-advice":
            return post_final_case_advice


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


class Finalise(LoginRequiredMixin, TemplateView):
    """
    Finalise a case and change the case status to finalised
    """

    @staticmethod
    def _get_goods(request, pk, case_type):
        goods = []
        if case_type == CaseType.STANDARD.value:
            goods, status_code = get_finalise_application_goods(request, pk)
            if status_code != HTTPStatus.OK:
                return error_page(request, FinaliseLicenceForm.GOODS_ERROR)
            goods = goods["goods"]
        return goods

    def get(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        case_type = case.data["case_type"]["sub_type"]["key"]

        if case_type == CaseType.OPEN.value:
            approve = get_open_licence_decision(request, str(kwargs["pk"])) == "approve"
            all_nlr = False
        else:
            advice = filter_advice_by_level(case["advice"], "final")
            items = [item["type"]["key"] for item in advice]
            approve = any([item == "approve" or item == "proviso" for item in items])
            all_nlr = not approve and "refuse" not in items

        case_id = case["id"]

        if approve:
            any_nlr = any([item == "no_licence_required" for item in items])
            licence_data, _ = get_licence(request, str(kwargs["pk"]))
            licence = licence_data.get("licence")
            # If there are licenced goods, we want to use the reissue goods flow.
            if licence:
                form, form_data = reissue_finalise_form(request, licence, case, kwargs["queue_pk"])
            else:
                goods = self._get_goods(request, str(kwargs["pk"]), case_type)
                form, form_data = finalise_form(request, case, goods, kwargs["queue_pk"])
            return form_page(
                request,
                form,
                data=form_data,
                extra_data={
                    "any_nlr": any_nlr,
                    "case": case,
                    "has_proviso": any([item == "proviso" for item in items]),
                },
            )
        else:
            return form_page(
                request,
                deny_licence_form(
                    kwargs["queue_pk"],
                    case_id,
                    case.data["case_type"]["sub_type"]["key"] == CaseType.OPEN.value,
                    all_nlr,
                ),
            )

    def post(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        application_id = case.data.get("id")
        data = request.POST.copy()

        res = finalise_application(request, application_id, data)
        licence_data, _ = get_licence(request, str(kwargs["pk"]))
        licence = licence_data.get("licence")

        if res.status_code == HTTPStatus.FORBIDDEN:
            return error_page(request, "You do not have permission.")

        if res.status_code != HTTPStatus.OK:
            # If there are licenced goods, we want to use the reissue goods flow.
            if licence:
                form, form_data = reissue_finalise_form(request, licence, case, kwargs["queue_pk"])
            else:
                goods = self._get_goods(request, str(kwargs["pk"]), case.data["case_type"]["sub_type"]["key"])
                form, form_data = finalise_form(request, case, goods, kwargs["queue_pk"])

            return form_page(request, form, data=form_data, errors=res.json()["errors"], extra_data={"case": case})

        return redirect(
            reverse_lazy(
                "cases:finalise_documents",
                kwargs={"queue_pk": kwargs["queue_pk"], "pk": case["id"]},
            )
        )


class FinaliseGenerateDocuments(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = generate_documents_form(kwargs["queue_pk"], self.object_pk)
        decisions, _ = get_final_decision_documents(request, self.object_pk)
        decisions = decisions["documents"]
        can_submit = all([decision.get("document") for decision in decisions.values()])
        self.context = {
            "case": case,
            "can_submit": can_submit,
            "decisions": decisions,
        }
        self.action = grant_licence
        self.success_message = GenerateGoodsDecisionForm.SUCCESS_MESSAGE
        self.success_url = reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})
