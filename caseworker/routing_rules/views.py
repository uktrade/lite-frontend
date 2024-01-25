from django.shortcuts import render
from django.views.generic import TemplateView

from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission, get_params_if_exist
from core.helpers import convert_dict_to_query_params
from caseworker.core.services import get_statuses
from lite_content.lite_internal_frontend.routing_rules import Filter
from lite_forms.components import FiltersBar, Option, Checkboxes, Select, AutocompleteInput, TextInput
from lite_forms.helpers import conditional
from caseworker.queues.services import get_queues
from caseworker.routing_rules.services import get_routing_rules
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
