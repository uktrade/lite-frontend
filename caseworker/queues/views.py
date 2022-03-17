from http import HTTPStatus

from django.views.generic.edit import CreateView
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

from caseworker.cases.forms.assign_users import assign_users_form
from caseworker.cases.helpers.filters import case_filters_bar
from caseworker.core.constants import (
    ALL_CASES_QUEUE_ID,
    Permission,
    UPDATED_CASES_QUEUE_ID,
    SLA_CIRCUMFERENCE,
    SLA_RADIUS,
)
from caseworker.core.services import get_user_permissions
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
from caseworker.queues.services import get_cases_search_data


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
        hidden = self.request.GET.get("hidden")

        params = {"page": int(self.request.GET.get("page", 1))}
        for key, value in self.request.GET.items():
            if key != "flags[]":
                params[key] = value

        params["flags"] = self.request.GET.getlist("flags[]", [])

        if hidden:
            params["hidden"] = hidden

        data = get_cases_search_data(self.request, self.queue_pk, params)
        return data

    @property
    def filters(self):
        return self.data["results"]["filters"]

    def get_context_data(self, *args, **kwargs):

        try:
            updated_queue = [
                queue for queue in self.data["results"]["queues"] if queue["id"] == UPDATED_CASES_QUEUE_ID
            ][0]
            show_updated_cases_banner = updated_queue["case_count"]
        except IndexError:
            show_updated_cases_banner = False

        is_system_queue = self.queue.get("is_system_queue", False)

        for case in self.data["results"]["cases"]:
            try:
                destinations = case["destinations"]
            except KeyError:
                destinations = []

            unique_destinations = [
                dict(t) for t in {tuple(destination["country"].items()) for destination in destinations}
            ]
            case["unique_destinations"] = unique_destinations

        context = {
            "sla_radius": SLA_RADIUS,
            "sla_circumference": SLA_CIRCUMFERENCE,
            "data": self.data,
            "queue": self.queue,  # Used for showing current queue
            "filters": case_filters_bar(self.request, self.filters, is_system_queue),
            "is_all_cases_queue": self.queue_pk == ALL_CASES_QUEUE_ID,
            "enforcement_check": Permission.ENFORCEMENT_CHECK.value in get_user_permissions(self.request),
            "updated_cases_banner_queue_id": UPDATED_CASES_QUEUE_ID,
            "show_updated_cases_banner": show_updated_cases_banner,
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
        }
        return render(request, "queues/manage.html", context)


class AddQueue(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.form = forms.new_queue_form(request)
        self.action = post_queues
        self.success_url = reverse_lazy("queues:manage")


class EditQueue(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)
        self.form = forms.edit_queue_form(request, self.object_pk)
        self.action = put_queue
        self.success_url = reverse_lazy("queues:manage")


class CaseAssignments(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case_ids = request.GET.getlist("cases")

        if not case_ids:
            return error_page(request, "Invalid case selection")

        queue = get_queue(request, self.object_pk)
        case_assignments, _ = get_queue_case_assignments(request, self.object_pk)
        assigned_users = [
            assignment["user"] for assignment in case_assignments["case_assignments"] if assignment["case"] in case_ids
        ]
        user_data, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))

        self.data = {"users": assigned_users}
        self.form = assign_users_form(request, user_data["user"]["team"]["id"], queue, len(case_ids) > 1)
        self.action = put_queue_case_assignments
        self.success_url = reverse("queues:cases", kwargs={"queue_pk": self.object_pk})
        self.success_message = (
            Manage.AssignUsers.SUCCESS_MULTI_MESSAGE if len(case_ids) > 1 else Manage.AssignUsers.SUCCESS_MESSAGE
        )


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
