from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

from dateutil import parser
from django.http import Http404
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import FormView

from caseworker.bookmarks.services import fetch_bookmarks
from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS, LU_PRE_CIRC_REVIEW_QUEUE_ALIAS
from caseworker.core.constants import (
    ALL_CASES_QUEUE_ID,
    Permission,
    UPDATED_CASES_QUEUE_ID,
    SLA_CIRCUMFERENCE,
    SLA_RADIUS,
)
from caseworker.core.services import get_regime_entries
from caseworker.core.services import get_user_permissions, get_control_list_entries
from caseworker.flags.services import get_flags
from caseworker.queues.services import get_cases_search_data, head_cases_search_count
from caseworker.queues.services import (
    get_queue,
)
from caseworker.queues.views.forms import CasesFiltersForm
from core.auth.views import LoginRequiredMixin
from core.exceptions import ServiceError
from lite_content.lite_internal_frontend.cases import CasesListPage


class CaseDataMixin:
    @cached_property
    def data(self):
        params = self.get_params()

        response = get_cases_search_data(self.request, self.queue_pk, params)
        if not response.ok:
            if response.status_code == 404:
                raise Http404()
            else:
                raise ServiceError(
                    message="Error retrieving cases data from lite-api",
                    status_code=502,
                    response=response,
                    log_message="Error retrieving cases data from lite-api",
                    user_message="A problem occurred. Please try again later",
                )

        return response.json()

    @cached_property
    def all_flags(self):
        return get_flags(self.request, disable_pagination=True)

    @cached_property
    def all_cles(self):
        return get_control_list_entries(self.request, include_parent=True)

    @cached_property
    def all_regimes(self):
        return get_regime_entries(self.request)

    @property
    def filters(self):
        gov_users = self.data["results"]["filters"]["gov_users"]
        filtered_gov_users = [gov_user for gov_user in gov_users if not gov_user["pending"]]

        self.data["results"]["filters"]["gov_users"] = filtered_gov_users

        return self.data["results"]["filters"]

    def get_params(self):
        params = {"page": int(self.request.GET.get("page", 1))}
        for key, value in self.request.GET.items():
            if key != "flags[]":  # What is this for? Thinking it is an artifact of times gone by...
                params[key] = value

        # this is essentially decomposing date fields
        # API expects individual fields for day, month, year for these filters
        # Crispy form gives us "submitted_from_{0..2}" so they are mapped to day, month, year
        # Usually this is done in clean() but it doesn't get called as we are not posting anything
        for param in ["submitted_from", "submitted_to", "finalised_from", "finalised_to"]:
            date_tokens = []
            for index, field in [(0, "day"), (1, "month"), (2, "year")]:
                key = f"{param}_{index}"
                if key in params:
                    updated_key = f"{param}_{field}"
                    params[updated_key] = params.get(key, "")
                    date_tokens.append(params[updated_key])

            # We need to save compressed date values to show the current filter value
            if date_tokens and all(date_tokens):
                date_str = "-".join(date_tokens)
                date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
                params[param] = date_obj

        params["flags"] = self.request.GET.getlist("flags", [])
        params["countries"] = self.request.GET.getlist("countries", [])
        params["assigned_queues"] = self.request.GET.getlist("assigned_queues", [])
        params["control_list_entry"] = self.request.GET.getlist("control_list_entry", [])
        params["regime_entry"] = self.request.GET.getlist("regime_entry", [])

        params["selected_tab"] = self.request.GET.get("selected_tab", CasesListPage.Tabs.ALL_CASES)

        # if the hidden param is 'true' then cases with open queries are included
        # it should be false on team queues for the 'all cases' tab
        # but it can be overriden by a checkbox on the frontend
        is_hidden_by_form = self.request.GET.get("hidden", False)
        params["hidden"] = self._set_is_hidden(params["selected_tab"], is_hidden_by_form)
        # Ideally we would do some proper form validation and this value would be removed
        # as part of that, until then we remove assigned_queues from the params
        # because this should not be filtered on unless the queue is a system queue
        if params.get("assigned_queues") and not self._is_system_queue():
            del params["assigned_queues"]

        # No need to send return_to parameter in server calls
        if params.get("return_to"):
            del params["return_to"]

        return params

    def _set_is_hidden(self, tab_name, is_hidden_by_form):
        if is_hidden_by_form:
            return "True"
        elif self._is_system_queue():
            return "True"
        elif tab_name == CasesListPage.Tabs.MY_CASES or tab_name == CasesListPage.Tabs.OPEN_QUERIES:
            return "True"
        else:
            return "False"

    def _is_system_queue(self):
        return self.queue.get("is_system_queue", False)

    @cached_property
    def queue(self):
        return get_queue(self.request, self.queue_pk)

    @property
    def queue_pk(self):
        return self.kwargs.get("queue_pk") or self.request.session["default_queue"]


class Cases(LoginRequiredMixin, CaseDataMixin, FormView):
    """
    Homepage
    """

    template_name = "queues/cases.html"
    form_class = CasesFiltersForm

    def _get_tab_url(self, tab_name):
        params = self.request.GET.copy()
        # Remove page from params to ensure page is reset when changing tabs
        if params.get("page"):
            del params["page"]
        params["selected_tab"] = tab_name
        return f"?{params.urlencode()}"

    def _get_tab_count(self, tab_name):
        is_hidden_by_form = self.request.GET.get("hidden", None)
        params = self.get_params()
        params["selected_tab"] = tab_name
        params["hidden"] = self._set_is_hidden(tab_name, is_hidden_by_form)

        return head_cases_search_count(self.request, self.queue_pk, params)

    def _tab_data(self):
        selected_tab = self.request.GET.get("selected_tab", CasesListPage.Tabs.ALL_CASES)
        tab_data = {}

        for tab in CasesListPage.Tabs:
            tab_data[tab] = {
                "count": self._get_tab_count(tab),
                "is_selected": selected_tab == tab,
                "url": self._get_tab_url(tab.value),
            }

        return tab_data

    def _transform_destinations(self, case):
        try:
            destinations = case["destinations"]
        except KeyError:
            destinations = []

        unique_destinations = [dict(t) for t in {tuple(destination["country"].items()) for destination in destinations}]
        return unique_destinations

    def _limit_lines(self, text, limit):
        lines = text.splitlines()
        if len(lines) > limit:
            lines = lines[:limit]
            lines[-1] += "..."
        return "\n".join(lines)

    def _transform_activity_updates(self, case):
        try:
            activity_updates = case["activity_updates"]
        except KeyError:
            activity_updates = []

        transformed_updates = []
        for update in activity_updates:
            if update["text"]:
                update["text"] = self._limit_lines(update["text"], 2)
            if update["additional_text"]:
                update["additional_text"] = self._limit_lines(update["additional_text"], 2)
            transformed_updates.append(update)

        return transformed_updates

    def _transform_queue_assignments(self, case):
        assigned_queues = {}
        for _, assignment in case["assignments"].items():
            for assigned_queue in assignment["queues"]:
                assignee = {k: v for k, v in assignment.items() if k != "queues"}
                try:
                    assigned_queues[assigned_queue["id"]]["assignees"].append(assignee)
                except KeyError:
                    assigned_queues[assigned_queue["id"]] = {
                        "queue_name": assigned_queue["name"],
                        "assignees": [{k: v for k, v in assignment.items() if k != "queues"}],
                    }

        queues_that_hide_assignments = (LU_PRE_CIRC_REVIEW_QUEUE_ALIAS, LU_POST_CIRC_FINALISE_QUEUE_ALIAS)
        all_queues = {}
        if self.queue["alias"] not in queues_that_hide_assignments:
            all_queues = {queue["id"]: {"queue_name": queue["name"], "assignees": []} for queue in case["queues"]}

        all_assignments = {**all_queues, **assigned_queues}

        return all_assignments

    def _transform_goods(self, case):
        goods_summary = {
            "cles": set(),
            "regimes": set(),
            "report_summaries": set(),
            "total_value": Decimal(),
        }
        for good in case["goods"]:
            goods_summary["cles"].update(good["cles"])
            goods_summary["regimes"].update(good["regimes"])
            if good["report_summary_subject"]:
                report_summary = good["report_summary_subject"]
                if good["report_summary_prefix"]:
                    report_summary = f"{good['report_summary_prefix']} {report_summary}"
                goods_summary["report_summaries"].add(report_summary)
            goods_summary["total_value"] += Decimal(good["value"])
        return goods_summary

    def transform_case(self, case):
        case["unique_destinations"] = self._transform_destinations(case)
        case["queue_assignments"] = self._transform_queue_assignments(case)
        case["activity_updates"] = self._transform_activity_updates(case)
        case["goods_summary"] = self._transform_goods(case)
        case["submitted_at"] = parser.parse(case["submitted_at"])

    def get_initial(self):
        return self.get_params()

    def _strip_param_from_url(self, url, param):
        url_parts = list(urlparse(url))
        query = parse_qs(url_parts[4], keep_blank_values=True)
        if query.get(param):
            del query[param]
        url_parts[4] = urlencode(query, doseq=True)
        sanitised_url = urlunparse(url_parts)
        return sanitised_url

    def get_return_url(self):
        current_full_url = self.request.get_full_path()
        sanitised_url = self._strip_param_from_url(current_full_url, "return_to")
        return sanitised_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["filters_data"] = self.filters
        kwargs["all_flags"] = self.all_flags
        kwargs["all_cles"] = self.all_cles
        kwargs["all_regimes"] = self.all_regimes
        kwargs["queue"] = self.queue
        kwargs["initial"]["return_to"] = self.get_return_url()
        return kwargs

    def post(self, request, *args, **kwargs):
        # This view does most of it's work through GET, but initial form POST submissions
        # are handled here and redirected to a GET after stripping out csrfmiddlewaretoken
        # - this should not be visible in GET params due to security concerns
        get_params = request.POST.urlencode()
        url = f"{request.path}?{get_params}"
        sanitised_url = self._strip_param_from_url(url, "csrfmiddlewaretoken")
        return redirect(sanitised_url)

    def get_context_data(self, *args, **kwargs):
        try:
            updated_queue = [
                queue for queue in self.data["results"]["queues"] if queue["id"] == UPDATED_CASES_QUEUE_ID
            ][0]
            show_updated_cases_banner = updated_queue["case_count"]
        except IndexError:
            show_updated_cases_banner = False

        for case in self.data["results"]["cases"]:
            self.transform_case(case)

        bookmarks = fetch_bookmarks(self.request, self.filters, self.all_flags, self.all_regimes, self.request.path)
        context = {
            "sla_radius": SLA_RADIUS,
            "sla_circumference": SLA_CIRCUMFERENCE,
            "data": self.data,
            "queue": self.queue,  # Used for showing current queue
            "is_all_cases_queue": self.queue_pk == ALL_CASES_QUEUE_ID,
            "enforcement_check": Permission.ENFORCEMENT_CHECK.value in get_user_permissions(self.request),
            "updated_cases_banner_queue_id": UPDATED_CASES_QUEUE_ID,
            "show_updated_cases_banner": show_updated_cases_banner,
            "tab_data": self._tab_data(),
            "bookmarks": bookmarks,
            "return_to": self.get_return_url(),
        }

        return super().get_context_data(*args, **context, **kwargs)
