from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission, get_params_if_exist
from core.helpers import convert_dict_to_query_params
from caseworker.core.services import get_statuses
from lite_content.lite_internal_frontend.routing_rules import Filter, CONFIRM_FORM_ERROR
from lite_forms.components import FiltersBar, Option, Checkboxes, Select, AutocompleteInput, TextInput
from lite_forms.generators import form_page
from lite_forms.helpers import conditional
from lite_forms.views import MultiFormView, SingleFormView
from caseworker.queues.services import get_queues
from caseworker.routing_rules.forms import (
    routing_rule_form_group,
    deactivate_or_activate_routing_rule_form,
)
from caseworker.routing_rules.services import (
    get_routing_rules,
    post_routing_rule,
    put_routing_rule_active_status,
    get_routing_rule,
    put_routing_rule,
    validate_put_routing_rule,
)
from caseworker.teams.services import get_teams, get_users_team_queues
from caseworker.users.services import get_gov_user

from core.auth.views import LoginRequiredMixin


class RoutingRulesList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        params = {
            "page": int(request.GET.get("page", 1)),
            **get_params_if_exist(request, ["case_status", "team", "queue", "tier", "only_active"]),
        }
        data, _ = get_routing_rules(request, convert_dict_to_query_params(params))

        user_data, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))

        status = request.GET.get("status", "active")

        filters = FiltersBar(
            [
                Select(title=Filter.CASE_STATUS, name="case_status", options=get_statuses(request, True)),
                *conditional(
                    has_permission(request, Permission.MANAGE_ALL_ROUTING_RULES),
                    [
                        Select(title=Filter.TEAM, name="team", options=get_teams(request, True)),
                        AutocompleteInput(
                            title=Filter.QUEUE,
                            name="queue",
                            options=get_queues(request, convert_to_options=True),
                        ),
                    ],
                    [
                        AutocompleteInput(
                            title=Filter.QUEUE,
                            name="queue",
                            options=get_users_team_queues(request, request.session["lite_api_user_id"], True),
                        ),
                    ],
                ),
                TextInput(title=Filter.TIER, name="tier"),
                Checkboxes(
                    name="only_active",
                    options=[Option(True, Filter.ACTIVE_ONLY)],
                    classes=["govuk-checkboxes--small"],
                ),
            ]
        )

        context = {
            "data": data,
            "status": status,
            "user_data": user_data,
            "filters": filters,
        }
        return render(request, "routing-rules/index.html", context)


class CreateRoutingRule(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        select_team = has_permission(request, Permission.MANAGE_ALL_ROUTING_RULES)
        team_id = request.POST.get("team", get_gov_user(request)[0]["user"]["team"]["id"])
        if not team_id:
            team_id = get_gov_user(request)[0]["user"]["team"]["id"]
        additional_rules = request.POST.getlist("additional_rules[]", ())
        flags_to_include = request.POST.getlist("flags_to_include")
        flags_to_exclude = request.POST.getlist("flags_to_exclude")
        self.forms = routing_rule_form_group(
            request,
            additional_rules,
            team_id,
            flags_to_include,
            flags_to_exclude,
            select_team=select_team,
        )
        self.success_url = reverse("routing_rules:list")
        self.action = post_routing_rule


class ChangeRoutingRuleActiveStatus(LoginRequiredMixin, SingleFormView):
    success_url = reverse_lazy("routing_rules:list")

    def init(self, request, **kwargs):
        status = kwargs["status"]
        self.object_pk = kwargs["pk"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        self.form = deactivate_or_activate_routing_rule_form(activate=status == "reactivate", status=status)
        self.action = put_routing_rule_active_status

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": [CONFIRM_FORM_ERROR]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(ChangeRoutingRuleActiveStatus, self).post(request, **kwargs)


class EditRoutingRules(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_routing_rule(request, self.object_pk)[0]
        team_id = self.data["team"]
        additional_rules = self.data.get("additional_rules", [])
        flags_to_include = self.data.get("flags_to_include", [])
        flags_to_exclude = self.data.get("flags_to_exclude", [])

        if request.method == "POST":
            additional_rules = request.POST.getlist("additional_rules[]", additional_rules)
            if "flags_to_include" in request.POST:
                flags_to_include = [flag for flag in request.POST.get("flags_to_include", []).split(",") if flag]
            if "flags_to_exclude" in request.POST:
                flags_to_exclude = [flag for flag in request.POST.get("flags_to_exclude", []).split(",") if flag]

            self.forms = routing_rule_form_group(
                request, additional_rules, team_id, flags_to_include, flags_to_exclude, is_editing=True
            )

            # we only want to update the data during the last form post
            if (len(self.get_forms().forms) - 1) == int(request.POST.get("form_pk", 0)):
                self.action = put_routing_rule
            else:
                self.action = validate_put_routing_rule

        else:
            self.forms = routing_rule_form_group(
                request, additional_rules, team_id, flags_to_include, flags_to_exclude, is_editing=True
            )
            self.action = put_routing_rule

        self.success_url = reverse_lazy("routing_rules:list")

    def get_data(self):
        data = self.data
        if "flags_to_include" in data:
            data["flags_to_include"] = ",".join(data["flags_to_include"])
        if "flags_to_exclude" in data:
            data["flags_to_exclude"] = ",".join(data["flags_to_exclude"])
        return data
