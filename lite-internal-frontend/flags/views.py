import functools

from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.helpers.advice import get_param_goods, get_param_destinations
from cases.services import put_flag_assignments, get_case
from conf.constants import Permission
from core.helpers import convert_dict_to_query_params, get_params_if_exist
from core.services import get_user_permissions
from flags.enums import FlagLevel, FlagStatus
from flags.forms import (
    add_flag_form,
    edit_flag_form,
    create_flagging_rules_formGroup,
    select_condition_and_flag,
    _levels,
    deactivate_or_activate_flagging_rule_form,
    level_options,
    set_flags_form,
)
from flags.helpers import get_matching_flags
from flags.services import (
    get_flagging_rules,
    put_flagging_rule,
    get_flagging_rule,
    post_flagging_rules,
    get_cases_flags,
    get_organisation_flags,
    get_goods_flags,
    get_destination_flags,
)
from flags.services import get_flags, post_flags, get_flag, update_flag
from lite_content.lite_internal_frontend import strings, flags
from lite_content.lite_internal_frontend.flags import UpdateFlag, SetFlagsForm
from lite_forms.components import Option, FiltersBar, Select, Checkboxes, TextInput, BackLink
from lite_forms.generators import form_page
from lite_forms.views import MultiFormView, SingleFormView
from organisations.services import get_organisation
from teams.services import get_teams
from users.services import get_gov_user


class FlagsList(TemplateView):
    def get(self, request, **kwargs):
        params = request.GET.copy()
        params["status"] = params.get("status", FlagStatus.ACTIVE.value)
        data = get_flags(request, **params)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

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
        }
        return render(request, "flags/index.html", context)


class AddFlag(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_flag_form()
        self.action = post_flags
        self.data = {"colour": "default", "priority": 0}
        self.success_message = flags.FlagsList.SUCCESS_MESSAGE
        self.success_url = reverse("flags:flags")


class EditFlag(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        flag = get_flag(request, self.object_pk)
        self.form = edit_flag_form()
        self.data = flag
        self.action = update_flag
        self.success_url = reverse("flags:flags")


class ChangeFlagStatus(TemplateView):
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


class ManageFlagRules(TemplateView):
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

        context = {
            "data": data,
            "page": params.pop("page"),
            "team": get_gov_user(request)[0]["user"]["team"]["id"],
            "filters": filters,
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "flags/flagging-rules-list.html", context)


class CreateFlagRules(MultiFormView):
    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        type = request.POST.get("level", None)
        self.forms = create_flagging_rules_formGroup(request=self.request, type=type)
        self.action = post_flagging_rules
        self.success_url = reverse_lazy("flags:flagging_rules")


class EditFlaggingRules(SingleFormView):
    def init(self, request, **kwargs):
        if Permission.MANAGE_FLAGGING_RULES.value not in get_user_permissions(request):
            return redirect(reverse_lazy("cases:cases"))

        self.object_pk = kwargs["pk"]
        self.data = get_flagging_rule(request, self.object_pk)[0]["flag"]
        self.form = select_condition_and_flag(request, type=self.data["level"])
        self.action = put_flagging_rule
        self.success_url = reverse_lazy("flags:flagging_rules")


class ChangeFlaggingRuleStatus(SingleFormView):
    success_url = reverse_lazy("flags:flagging_rules")

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


def perform_action(level, request, pk, json):
    data = {
        "level": level,
        "objects": [
            x
            for x in [
                request.GET.get("case"),
                request.GET.get("organisation"),
                *request.GET.getlist("goods"),
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


class AssignFlags(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.level = self.get_level()
        flags = self.get_potential_flags()
        self.success_message = getattr(SetFlagsForm, self.level).SUCCESS_MESSAGE

        if self.level == FlagLevel.ORGANISATIONS:
            self.context = {"organisation": "123"}
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
                url=reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})
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
        return functools.partial(perform_action, self.level)

    def get_success_url(self):
        if self.request.GET.get("return_to"):
            return self.request.GET.get("return_to")
        elif self.level == FlagLevel.ORGANISATIONS:
            return reverse("organisations:organisation", kwargs={"pk": self.object_pk})
        else:
            return reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})
