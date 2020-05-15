from collections import defaultdict
from datetime import date
from http import HTTPStatus

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.constants import CaseType
from cases.forms.advice import give_advice_form, finalise_goods_countries_form, generate_documents_form
from cases.forms.finalise_case import approve_licence_form, deny_licence_form
from cases.helpers.advice import get_param_destinations, get_param_goods, flatten_advice_data, prepare_data_for_advice
from cases.services import (
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
    get_application_default_duration,
    grant_licence,
    get_final_decision_documents,
    get_licence,
    get_finalise_application_goods,
    post_good_countries_decisions,
)
from conf.constants import Permission
from core import helpers
from core.builtins.custom_tags import filter_advice_by_level
from core.services import get_denial_reasons
from lite_content.lite_internal_frontend.advice import FinaliseLicenceForm
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView


class GiveAdvice(SingleFormView):
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
            show_warning=not self.data,
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


class CoalesceUserAdvice(TemplateView):
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


class ClearTeamAdvice(TemplateView):
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


class CoalesceTeamAdvice(TemplateView):
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


class ClearFinalAdvice(TemplateView):
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


class FinaliseGoodsCountries(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {
            "case": case,
        }
        self.form = finalise_goods_countries_form(**kwargs)
        self.action = post_good_countries_decisions
        self.success_url = reverse_lazy("cases:finalise", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})

    def clean_data(self, data):
        selection = {"good_countries": []}
        data.pop("csrfmiddlewaretoken")
        data.pop("_action")

        for key, value in data.items():
            selection["good_countries"].append(
                {
                    "case": str(self.kwargs["pk"]),
                    "good": key.split(".")[0],
                    "country": key.split(".")[1],
                    "decision": value,
                }
            )

        return selection


class Finalise(TemplateView):
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
        case_type = case["application"]["case_type"]["sub_type"]["key"]
        is_case_oiel_final_advice_only = False
        if "goodstype_category" in case["application"]:
            is_case_oiel_final_advice_only = case["application"]["goodstype_category"]["key"] in [
                "media",
                "cryptographic",
                "dealer",
                "uk_continental_shelf",
            ]

        if case_type == CaseType.OPEN.value and not is_case_oiel_final_advice_only:
            data = get_good_countries_decisions(request, str(kwargs["pk"]))["data"]
            items = [item["decision"]["key"] for item in data]
            is_open_licence = True
        else:
            advice = filter_advice_by_level(case["advice"], "final")
            items = [item["type"]["key"] for item in advice]
            is_open_licence = case_type == CaseType.OPEN.value

        case_id = case["id"]
        duration = get_application_default_duration(request, str(kwargs["pk"]))

        if "approve" in items or "proviso" in items:
            # Redirect if licence already exists
            _, status_code = get_licence(request, str(kwargs["pk"]))
            if status_code == HTTPStatus.OK:
                return redirect(
                    reverse_lazy(
                        "cases:finalise_documents", kwargs={"queue_pk": kwargs["queue_pk"], "pk": str(kwargs["pk"])}
                    )
                )

            today = date.today()
            form_data = {
                "day": today.day,
                "month": today.month,
                "year": today.year,
                "duration": duration,
            }

            form = approve_licence_form(
                queue_pk=kwargs["queue_pk"],
                case_id=case_id,
                is_open_licence=is_open_licence,
                duration=duration,
                editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
                goods=self._get_goods(request, str(kwargs["pk"]), case_type),
            )
            return form_page(request, form, data=form_data, extra_data={"case": case})
        else:
            return form_page(request, deny_licence_form(kwargs["queue_pk"], case_id, is_open_licence))

    def post(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        is_open_licence = case["application"]["case_type"]["sub_type"]["key"] == CaseType.OPEN.value
        application_id = case.get("application").get("id")
        data = request.POST.copy()

        has_permission = helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION)

        res = finalise_application(request, application_id, data)

        if res.status_code == HTTPStatus.FORBIDDEN:
            return error_page(request, "You do not have permission.")

        if res.status_code == HTTPStatus.BAD_REQUEST:
            case_type = case["application"]["case_type"]["sub_type"]["key"]
            form = approve_licence_form(
                queue_pk=kwargs["queue_pk"],
                case_id=case["id"],
                is_open_licence=is_open_licence,
                duration=data.get("licence_duration") or get_application_default_duration(request, str(kwargs["pk"])),
                editable_duration=has_permission,
                goods=self._get_goods(request, str(kwargs["pk"]), case_type),
            )
            return form_page(request, form, data=data, errors=res.json()["errors"], extra_data={"case": case})

        return redirect(
            reverse_lazy("cases:finalise_documents", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case["id"]})
        )


class FinaliseGenerateDocuments(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = generate_documents_form()
        decisions, _ = get_final_decision_documents(request, self.object_pk)
        decisions = decisions["documents"]
        can_submit = all([decision.get("document") for decision in decisions.values()])
        self.context = {
            "case": case,
            "can_submit": can_submit,
            "decisions": decisions,
        }
        self.action = grant_licence
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": "final-advice"}
        )
