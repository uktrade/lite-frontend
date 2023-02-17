from http import HTTPStatus
from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.utils.functional import cached_property

from lite_content.lite_internal_frontend.cases import CasesListPage, Manage
from lite_forms.components import TextInput, FiltersBar
from lite_forms.generators import error_page
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from caseworker.cases.helpers.filters import case_filters_bar
from caseworker.core.constants import (
    ALL_CASES_QUEUE_ID,
    Permission,
    UPDATED_CASES_QUEUE_ID,
    SLA_CIRCUMFERENCE,
    SLA_RADIUS,
)
from caseworker.core.services import get_user_permissions
from caseworker.core.helpers import is_user_config_admin
from caseworker.core.views import handler403
from caseworker.queues import forms
from caseworker.queues.services import (
    get_queues,
    post_queues,
    get_queue,
    put_queue,
    get_queue_case_assignments,
    put_queue_case_assignments,
    get_enforcement_xml,
    post_enforcement_xml,
)
from caseworker.users.services import get_gov_user
from caseworker.queues.services import get_cases_search_data, head_cases_search_count
from caseworker.cases.services import update_case_officer_on_cases
from caseworker.queues.forms import SelectAllocateRole


class Cases(LoginRequiredMixin, TemplateView):
    """
    Homepage
    """

    template_name = "queues/cases.html"

    @cached_property
    def queue(self):
        return get_queue(self.request, self.queue_pk)

    @property
    def queue_pk(self):
        return self.kwargs.get("queue_pk") or self.request.session["default_queue"]

    @cached_property
    def data(self):
        params = self.get_params()

        data = get_cases_search_data(self.request, self.queue_pk, params)
        return data

    @property
    def filters(self):
        return self.data["results"]["filters"]

    def get_params(self):
        params = {"page": int(self.request.GET.get("page", 1))}
        for key, value in self.request.GET.items():
            if key != "flags[]":
                params[key] = value

        params["flags"] = self.request.GET.getlist("flags[]", [])

        params["selected_tab"] = self.request.GET.get("selected_tab", CasesListPage.Tabs.ALL_CASES)

        # if the hidden param is 'true' then cases with open queries are included
        # it should be false on team queues for the 'all cases' tab
        # but it can be overriden by a checkbox on the frontend
        is_hidden_by_form = self.request.GET.get("hidden", False)
        params["hidden"] = self._set_is_hidden(params["selected_tab"], is_hidden_by_form)

        return params

    def _get_tab_url(self, tab_name):
        params = self.request.GET.copy()
        params["selected_tab"] = tab_name
        return f"?{params.urlencode()}"

    def _get_tab_count(self, tab_name):
        is_hidden_by_form = self.request.GET.get("hidden", None)
        params = self.get_params()
        params["selected_tab"] = tab_name
        params["hidden"] = self._set_is_hidden(tab_name, is_hidden_by_form)

        return head_cases_search_count(self.request, self.queue_pk, params)

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

        all_queues = {queue["id"]: {"queue_name": queue["name"], "assignees": []} for queue in case["queues"]}

        all_assignments = {**all_queues, **assigned_queues}

        return all_assignments

    def transform_case(self, case):
        case["unique_destinations"] = self._transform_destinations(case)
        case["queue_assignments"] = self._transform_queue_assignments(case)
        case["activity_updates"] = self._transform_activity_updates(case)

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

        context = {
            "sla_radius": SLA_RADIUS,
            "sla_circumference": SLA_CIRCUMFERENCE,
            "data": self.data,
            "queue": self.queue,  # Used for showing current queue
            "filters": case_filters_bar(self.request, self.filters, self._is_system_queue()),
            "is_all_cases_queue": self.queue_pk == ALL_CASES_QUEUE_ID,
            "enforcement_check": Permission.ENFORCEMENT_CHECK.value in get_user_permissions(self.request),
            "updated_cases_banner_queue_id": UPDATED_CASES_QUEUE_ID,
            "show_updated_cases_banner": show_updated_cases_banner,
            "tab_data": self._tab_data(),
        }

        return super().get_context_data(*args, **context, **kwargs)


class QueuesList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        page = request.GET.get("page", 1)
        name = request.GET.get("name")
        queues = get_queues(request, page=page, disable_pagination=False, name=name)
        user_data, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))

        filters = FiltersBar([TextInput(name="name", title="name")])

        context = {
            "data": queues,
            "user_data": user_data,
            "filters": filters,
            "name": name,
            "can_change_config": user_data["user"]["email"] in settings.CONFIG_ADMIN_USERS_LIST,
        }
        return render(request, "queues/manage.html", context)


class AddQueue(LoginRequiredMixin, SingleFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        self.form = forms.new_queue_form(request)
        self.action = post_queues
        self.success_url = reverse_lazy("queues:manage")


class EditQueue(LoginRequiredMixin, SingleFormView):
    def dispatch(self, request, *args, **kwargs):
        if not is_user_config_admin(request):
            return handler403(request, HttpResponseForbidden)

        return super().dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)
        self.form = forms.edit_queue_form(request, self.object_pk)
        self.action = put_queue
        self.success_url = reverse_lazy("queues:manage")


class CaseAssignmentSelectRole(LoginRequiredMixin, FormView):

    template_name = "core/form.html"
    form_class = SelectAllocateRole

    def _set_success_url(self, form):
        encoded_query_params = self.request.GET.urlencode()
        if form.cleaned_data["role"] == SelectAllocateRole.RoleChoices.CASE_ADVISOR.value:
            self.success_url = (
                reverse(f"queues:case_assignments_assign_user", kwargs={"pk": self.kwargs["pk"]})
                + f"?{encoded_query_params}"
            )
        else:
            self.success_url = (
                reverse(f"queues:case_assignments_assign_case_officer", kwargs={"pk": self.kwargs["pk"]})
                + f"?{encoded_query_params}"
            )

    def form_valid(self, form):
        self._set_success_url(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = {
            "back_link_url": reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]}),
            "title": self.form_class.Layout.TITLE,
        }
        return super().get_context_data(*args, **context, **kwargs)


class CaseAssignmentUsers(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.CaseAssignmentUsersForm
    success_message = "Case adviser allocated successfully"

    def get_form_kwargs(self):
        user_data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))

        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["team_id"] = user_data["user"]["team"]["id"]
        return form_kwargs

    def form_valid(self, form):
        # TODO
        #   - if initiated from a system queue; next step should be a multiuser version of /queues/{system_queue_id}/cases/{case_id}/assign-user-queue/{govuser_id}/
        #   - if queue already determined; this view should put the assignment and redirect
        queue = get_queue(self.request, self.kwargs["pk"])
        if queue["is_system_queue"]:
            params = {"cases": self.request.GET.getlist("cases"), **form.cleaned_data}
            queryparams = urlencode(params, doseq=True)
            next_url = (
                reverse("queues:case_assignments_assign_user_select_queue", kwargs={"pk": self.kwargs["pk"]})
                + f"?{queryparams}"
            )
            return HttpResponseRedirect(next_url)
        else:
            self.update_case_adviser(form.cleaned_data)
        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error updating case adviser on cases",
        "Unexpected error updating case adviser on cases",
    )
    def update_case_adviser(self, cleaned_data):
        case_ids = self.request.GET.getlist("cases")
        note = cleaned_data["note"]
        user_ids = cleaned_data["users"]
        return put_queue_case_assignments(self.request, self.kwargs["pk"], case_ids, user_ids, note)

    def get_success_url(self):
        # TODO: success URL to go back to case detail OR queue page
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})

    def get_context_data(self, *args, **kwargs):
        default_return_to_url = (
            reverse("queues:case_assignment_select_role", kwargs={"pk": self.kwargs["pk"]})
            + f"?{self.request.GET.urlencode()}"
        )
        return_to_url = self.request.GET.get("return_to", default_return_to_url)
        context = {
            "back_link_url": return_to_url,
            "title": self.form_class.Layout.TITLE,
        }
        return super().get_context_data(*args, **context, **kwargs)


class CaseAssignmentUsersSelectQueue(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.CaseAssignmentUsersSelectQueueForm
    success_message = "Case adviser allocated successfully"

    def get_form_kwargs(self):
        user_data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))

        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["user_id"] = user_data["user"]["id"]
        return form_kwargs

    def form_valid(self, form):
        self.update_case_adviser(form.cleaned_data)
        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error updating case adviser on cases",
        "Unexpected error updating case adviser on cases",
    )
    def update_case_adviser(self, cleaned_data):
        case_ids = self.request.GET.getlist("cases")
        user_ids = self.request.GET.getlist("users")
        note = self.request.GET.getlist("note")
        queue_id = cleaned_data["queue"]
        return put_queue_case_assignments(self.request, queue_id, case_ids, user_ids, note)

    def get_success_url(self):
        # TODO: success URL to go back to case detail OR queue page
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})

    def get_context_data(self, *args, **kwargs):
        return_to_url = self.request.GET.get("return_to")
        context = {
            "back_link_url": return_to_url,
            "title": self.form_class.Layout.TITLE,
        }
        return super().get_context_data(*args, **context, **kwargs)


class CaseAssignmentCaseOfficer(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.CaseAssignmentCaseOfficerForm
    success_message = "Licensing Unit case officer allocated successfully"

    def get_form_kwargs(self):
        user_data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))

        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["team_id"] = user_data["user"]["team"]["id"]
        return form_kwargs

    def form_valid(self, form):
        self.update_case_officer(form.cleaned_data["users"])
        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error updating case advisor on cases",
        "Unexpected error updating case advisor on cases",
    )
    def update_case_officer(self, user_id):
        case_ids = self.request.GET.getlist("cases")
        return update_case_officer_on_cases(self.request, case_ids, user_id)

    def get_success_url(self):
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})

    def get_context_data(self, *args, **kwargs):
        context = {
            "back_link_url": reverse("queues:case_assignment_select_role", kwargs={"pk": self.kwargs["pk"]})
            + f"?{self.request.GET.urlencode()}",
            "title": self.form_class.Layout.TITLE,
        }
        return super().get_context_data(*args, **context, **kwargs)


class EnforcementXMLExport(LoginRequiredMixin, TemplateView):
    def get(self, request, pk):
        data, status_code = get_enforcement_xml(request, pk)

        if status_code == HTTPStatus.NO_CONTENT:
            return error_page(request, CasesListPage.EnforcementXML.Export.NO_CASES)
        elif status_code != HTTPStatus.OK:
            return error_page(request, CasesListPage.EnforcementXML.Export.GENERIC_ERROR)
        else:
            return data


class EnforcementXMLImport(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "queues/enforcement-xml-import.html"
    form_class = forms.EnforcementXMLImportForm
    success_message = "Enforcement XML imported successfully"

    def form_valid(self, form):
        response = post_enforcement_xml(request=self.request, queue_pk=self.kwargs["pk"], json=form.cleaned_data)
        if not response.ok:
            for key, errors in response.json()["errors"].items():
                for error in errors:
                    form.add_error(key, error)
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()
