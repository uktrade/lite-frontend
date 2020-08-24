from http import HTTPStatus

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from caseworker.cases.forms.assign_users import assign_users_form
from caseworker.cases.forms.attach_documents import upload_document_form
from caseworker.cases.helpers.filters import case_filters_bar
from caseworker.core.constants import ALL_CASES_QUEUE_ID, Permission, UPDATED_CASES_QUEUE_ID
from core.helpers import convert_parameters_to_query_params
from caseworker.core.services import get_user_permissions
from lite_content.lite_internal_frontend.cases import CasesListPage, UploadEnforcementXML, Manage
from lite_forms.components import TextInput, FiltersBar
from lite_forms.generators import error_page
from lite_forms.views import SingleFormView
from caseworker.queues.forms import new_queue_form, edit_queue_form
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

from core.auth.views import LoginRequiredMixin


class Cases(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to the given queue
        """
        queue_pk = kwargs.get("queue_pk") or request.session["default_queue"]
        queue = get_queue(request, queue_pk)

        context = {
            "queue": queue,  # Used for showing current queue
            "filters": case_filters_bar(request, queue),
            "params": convert_parameters_to_query_params(request.GET),  # Used for passing params to JS
            "case_officer": request.GET.get("case_officer"),  # Used for reading params dynamically
            "assigned_user": request.GET.get("assigned_user"),  # ""
            "team_advice_type": request.GET.get("team_advice_type"),  # ""
            "final_advice_type": request.GET.get("final_advice_type"),  # ""
            "is_all_cases_queue": queue_pk == ALL_CASES_QUEUE_ID,
            "enforcement_check": Permission.ENFORCEMENT_CHECK.value in get_user_permissions(request),
            "updated_cases_banner_queue_id": UPDATED_CASES_QUEUE_ID,
        }
        return render(request, "queues/cases.html", context)


class QueuesList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        page = request.GET.get("page", 1)
        name = request.GET.get("name")
        queues = get_queues(request, page=page, disable_pagination=False, name=name)
        user_data, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))

        filters = FiltersBar([TextInput(name="name", title="name"),])

        context = {
            "data": queues,
            "user_data": user_data,
            "filters": filters,
            "name": name,
        }
        return render(request, "queues/manage.html", context)


class AddQueue(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.form = new_queue_form(request)
        self.action = post_queues
        self.success_url = reverse_lazy("queues:manage")


class EditQueue(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)
        self.form = edit_queue_form(request, self.object_pk)
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


class EnforcementXMLImport(LoginRequiredMixin, SingleFormView):
    def init(self, request, pk):
        self.object_pk = str(pk)
        self.form = upload_document_form(self.object_pk)
        self.action = post_enforcement_xml

    def get_success_url(self):
        messages.success(self.request, UploadEnforcementXML.SUCCESS_BANNER)
        return reverse_lazy("queues:enforcement_xml_import", kwargs={"pk": self.object_pk})
