import functools

from django.conf import settings
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from caseworker.cases.helpers.advice import get_param_goods, get_param_destinations
from caseworker.cases.services import put_flag_assignments, get_case
from caseworker.core.constants import Permission
from caseworker.core.helpers import get_params_if_exist, is_user_config_admin
from core.helpers import convert_dict_to_query_params
from caseworker.core.views import handler403
from caseworker.core.services import get_countries, get_user_permissions
from caseworker.flags.enums import FlagLevel, FlagStatus
from caseworker.flags.forms import (
    add_flag_form,
    edit_flag_form,
    create_flagging_rules_formGroup,
    select_condition_and_flag,
    _levels,
    deactivate_or_activate_flagging_rule_form,
    level_options,
    set_flags_form,
)
from caseworker.flags.helpers import get_matching_flags
from caseworker.flags.services import (
    get_flagging_rules,
    put_flagging_rule,
    get_flagging_rule,
    post_flagging_rules,
    get_cases_flags,
    get_organisation_flags,
    get_goods_flags,
    get_destination_flags,
)
from caseworker.flags.services import get_flags, post_flags, get_flag, update_flag
from lite_content.lite_internal_frontend import strings, flags
from lite_content.lite_internal_frontend.flags import UpdateFlag, SetFlagsForm
from lite_forms.components import Option, FiltersBar, Select, Checkboxes, TextInput, BackLink
from lite_forms.generators import form_page
from lite_forms.views import MultiFormView, SingleFormView
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


class AddFlag(LoginRequiredMixin, SingleFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        self.form = add_flag_form()
        self.action = post_flags
        self.data = {"colour": "default", "priority": 0}
        self.success_message = flags.FlagsList.SUCCESS_MESSAGE
        self.success_url = reverse("flags:flags")


class EditFlag(LoginRequiredMixin, SingleFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        flag = get_flag(request, self.object_pk)
        self.form = edit_flag_form()
        self.data = flag
        self.action = update_flag
        self.success_url = reverse("flags:flags")


class ChangeFlagStatus(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = UpdateFlag.Status.DEACTIVATE_WARNING

        if status == "reactivate":
            description = UpdateFlag.Status.REACTIVATE_WARNING

        context = {
            "title": "Are you sure you want to {} this flag?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "flags/change-status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        update_flag(request, str(kwargs["pk"]), json={"status": request.POST["status"]})

        return redirect(reverse_lazy("flags:flags"))


class ManageFlagRules(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        params = {"page": int(request.GET.get("page", 1))}
        params = get_params_if_exist(request, ["only_my_team", "level", "include_deactivated"], params)

        data, _ = get_flagging_rules(request, convert_dict_to_query_params(params))

        filters = FiltersBar(
            [
                Select(name="level", title=strings.FlaggingRules.List.Filter.Type, options=_levels),
                Checkboxes(
                    name="only_my_team",
                    options=[Option("true", strings.FlaggingRules.List.Filter.MY_TEAM_ONLY)],
                    classes=["govuk-checkboxes--small", "govuk-!-margin-top-6"],
                ),
                Checkboxes(
                    name="include_deactivated",
                    options=[Option("true", strings.FlaggingRules.List.Filter.INCLUDE_DEACTIVATED)],
                    classes=["govuk-checkboxes--small", "govuk-!-margin-top-6"],
                ),
            ]
        )

        user_data = get_gov_user(request)[0]["user"]

        countries, _ = get_countries(request)
        countries_map = {country["id"]: country["name"] for country in countries["countries"]}
        for rule in data["results"]:
            if rule["level"] == "Destination":
                rule["matching_values"] = [countries_map[id] for id in rule["matching_values"]]

        context = {
            "data": data,
            "team": user_data["team"]["id"],
            "filters": filters,
            "can_change_config": user_data["email"] in settings.CONFIG_ADMIN_USERS_LIST,
        }
        return render(request, "flags/flagging-rules-list.html", context)


class CreateFlagRules(LoginRequiredMixin, MultiFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        type = request.POST.get("level", None)
        self.forms = create_flagging_rules_formGroup(request=self.request, type=type)
        self.action = post_flagging_rules
        self.success_url = reverse_lazy("flags:flagging_rules")


class EditFlaggingRules(LoginRequiredMixin, SingleFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        self.object_pk = kwargs["pk"]
        self.data = get_flagging_rule(request, self.object_pk)[0]["flag"]
        self.form = select_condition_and_flag(request, type=self.data["level"])
        self.form.buttons[0].value = "Edit flagging rule"
        self.action = put_flagging_rule
        self.success_url = reverse_lazy("flags:flagging_rules")

    @cached_property
    def get_countries(self):
        countries, _ = get_countries(self.request)
        return countries["countries"]

    def get_data(self):
        if self.data["level"] == "Destination":
            countries_map = {country["id"]: country["name"] for country in self.get_countries}
            self.data["matching_values"] = [countries_map[id] for id in self.data["matching_values"]]

        return self.data

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()

        if "status" not in copied_request:
            copied_request["status"] = self.data["status"]
        # if the Tokenfields are empty then it is not being included in the request data
        if "matching_values[]" not in copied_request:
            copied_request.setlist("matching_values[]", [])
        if self.data["level"] == "Good" and "matching_groups[]" not in copied_request:
            copied_request.setlist("matching_groups[]", [])
        if self.data["level"] == "Good" and "excluded_values[]" not in copied_request:
            copied_request.setlist("excluded_values[]", [])

        if self.data["level"] == "Destination":
            reverse_countries_map = {country["name"]: country["id"] for country in self.get_countries}
            country_ids = [
                reverse_countries_map[name] if name in reverse_countries_map else name
                for name in copied_request.getlist("matching_values[]")
            ]
            copied_request.setlist("matching_values[]", country_ids)

        return copied_request


class ChangeFlaggingRuleStatus(LoginRequiredMixin, SingleFormView):
    success_url = reverse_lazy("flags:flagging_rules")

    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        status = kwargs["status"]
        self.object_pk = kwargs["pk"]

        if status != "Deactivated" and status != "Active":
            raise Http404

        if status == "Deactivated":
            title = strings.FlaggingRules.Status.DEACTIVATE_HEADING
            description = strings.FlaggingRules.Status.DEACTIVATE_WARNING
            confirm_text = strings.FlaggingRules.Status.DEACTIVATE_CONFIRM

        if status == "Active":
            title = strings.FlaggingRules.Status.REACTIVATE_HEADING
            description = strings.FlaggingRules.Status.REACTIVATE_WARNING
            confirm_text = strings.FlaggingRules.Status.REACTIVATE_CONFIRM

        self.form = deactivate_or_activate_flagging_rule_form(
            title=title, description=description, confirm_text=confirm_text, status=status
        )
        self.action = put_flagging_rule

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": [strings.FlaggingRules.Status.NO_SELECTION_ERROR]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(ChangeFlaggingRuleStatus, self).post(request, **kwargs)


def perform_action(case, level, request, pk, json):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types"))
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
