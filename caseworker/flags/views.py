import functools

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from caseworker.cases.helpers.advice import get_param_goods, get_param_destinations
from caseworker.cases.services import put_flag_assignments, get_case
from caseworker.core.constants import Permission
from caseworker.core.services import get_user_permissions
from caseworker.flags.enums import FlagLevel, FlagStatus
from caseworker.flags.forms import (
    level_options,
    set_flags_form,
)
from caseworker.flags.helpers import get_matching_flags
from caseworker.flags.services import (
    get_cases_flags,
    get_organisation_flags,
    get_goods_flags,
    get_destination_flags,
)
from caseworker.flags.services import get_flags
from lite_content.lite_internal_frontend import flags
from lite_content.lite_internal_frontend.flags import SetFlagsForm
from lite_forms.components import Option, FiltersBar, Select, Checkboxes, TextInput, BackLink
from lite_forms.views import SingleFormView
from caseworker.organisations.services import get_organisation
from caseworker.teams.services import get_teams
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin


class FlagsList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        params = request.GET.copy()
        params["status"] = params.get("status", FlagStatus.ACTIVE.value)
        data = get_flags(request, **params)
        user_data, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))

        filters = FiltersBar(
            [
                TextInput(name="name", title="name"),
                Select(name="level", title="level", options=level_options),
                TextInput(name="priority", title="priority"),
                Select(name="team", title="team", options=get_teams(request, True)),
                Checkboxes(
                    name="status",
                    options=[Option(FlagStatus.DEACTIVATED.value, flags.FlagsList.SHOW_DEACTIVATED_FLAGS)],
                    classes=["govuk-checkboxes--small"],
                ),
            ]
        )

        context = {
            "data": data,
            "user_data": user_data,
            "filters": filters,
            "can_change_flag_status": Permission.ACTIVATE_FLAGS.value in get_user_permissions(request),
            "can_change_config": user_data["user"]["email"] in settings.CONFIG_ADMIN_USERS_LIST,
        }
        return render(request, "flags/index.html", context)


def perform_action(case, level, request, pk, json):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types", []))
    product_ids = [item["good"]["id"] for item in goods if item["id"] in selected_goods_ids]
    data = {
        "level": level,
        "objects": [
            x
            for x in [
                request.GET.get("case"),
                request.GET.get("organisation"),
                *product_ids,
                *request.GET.getlist("goods_types"),
                *request.GET.getlist("countries"),
                request.GET.get("end_user"),
                request.GET.get("consignee"),
                *request.GET.getlist("third_party"),
                *request.GET.getlist("ultimate_end_user"),
            ]
            if x
        ],
        "flags": json.get("flags", []),
        "note": json.get("note"),
    }
    return put_flag_assignments(request, data)


class AssignFlags(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.level = self.get_level()
        flags = self.get_potential_flags()
        self.success_message = getattr(SetFlagsForm, self.level).SUCCESS_MESSAGE

        if self.level == FlagLevel.ORGANISATIONS:
            self.form = set_flags_form(flags, self.level)
            self.form.back_link = BackLink(url=reverse("organisations:organisation", kwargs={"pk": self.object_pk}))
        else:
            self.case = get_case(request, self.object_pk)
            self.context = {"case": self.case, "hide_flags_row": True}
            show_sidebar = False

            if self.level == FlagLevel.GOODS or self.level == FlagLevel.DESTINATIONS:
                show_sidebar = True
                self.context["goods"] = get_param_goods(self.request, self.case)
                self.context["destinations"] = get_param_destinations(self.request, self.case)

            self.form = set_flags_form(flags, self.level, show_case_header=True, show_sidebar=show_sidebar)
            self.form.back_link = BackLink(
                url=reverse(
                    "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": "details"}
                )
            )

        self.data = {"flags": self.get_object_flags()}

    def get_level(self):
        if self.request.GET.get("case"):
            return FlagLevel.CASES
        elif self.request.GET.get("organisation"):
            return FlagLevel.ORGANISATIONS
        elif self.request.GET.get("goods") or self.request.GET.get("goods_types"):
            return FlagLevel.GOODS
        else:
            return FlagLevel.DESTINATIONS

    def get_object_flags(self):
        if self.level == FlagLevel.CASES:
            return get_case(self.request, self.object_pk)["flags"]
        elif self.level == FlagLevel.ORGANISATIONS:
            return get_organisation(self.request, self.object_pk)["flags"]
        elif self.level == FlagLevel.GOODS:
            goods = get_param_goods(self.request, self.case)
            return get_matching_flags(goods)
        elif self.level == FlagLevel.DESTINATIONS:
            destinations = get_param_destinations(self.request, self.case)
            return get_matching_flags(destinations)

    def get_potential_flags(self):
        if self.level == FlagLevel.CASES:
            return get_cases_flags(self.request)
        elif self.level == FlagLevel.ORGANISATIONS:
            return get_organisation_flags(self.request)
        elif self.level == FlagLevel.GOODS:
            return get_goods_flags(self.request)
        elif self.level == FlagLevel.DESTINATIONS:
            return get_destination_flags(self.request)

    def get_action(self):
        return functools.partial(perform_action, self.case, self.level)

    def get_success_url(self):
        if self.request.GET.get("return_to"):
            return self.request.GET.get("return_to")
        elif self.level == FlagLevel.ORGANISATIONS:
            return reverse("organisations:organisation", kwargs={"pk": self.object_pk})
        elif self.level == FlagLevel.GOODS:
            return (
                reverse(
                    "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "details"}
                )
                + "#slice-goods"
            )
        elif self.level == FlagLevel.DESTINATIONS:
            return (
                reverse(
                    "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "details"}
                )
                + "#slice-destinations"
            )
        else:
            return reverse(
                "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "details"}
            )
