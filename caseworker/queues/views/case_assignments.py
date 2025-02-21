from http import HTTPStatus

from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.helpers import check_url
from core.wizard.views import BaseSessionWizardView

from caseworker.cases.views.main import CaseContextBasicMixin
from caseworker.queues import forms
from caseworker.queues.services import (
    put_queue_case_assignments,
)
from caseworker.users.services import get_gov_user
from caseworker.queues.conditionals import is_queue_in_url_system_queue
from caseworker.cases.services import update_case_officer_on_cases, get_case
from caseworker.queues.forms import SelectAllocateRole


class CaseAssignmentAllocateRole(LoginRequiredMixin, CaseContextBasicMixin, FormView):
    template_name = "core/form.html"
    form_class = SelectAllocateRole

    def form_valid(self, form):
        url_view_name = (
            "case_assignments_assign_user"
            if form.cleaned_data["role"] == SelectAllocateRole.RoleChoices.CASE_ADVISOR.value
            else "case_assignments_case_officer"
        )
        self.success_url = (
            reverse(f"queues:{url_view_name}", kwargs={"pk": self.kwargs["pk"]}) + f"?{self.request.GET.urlencode()}"
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = {
            "back_link_url": reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]}),
            "title": f"{self.form_class.Layout.DOCUMENT_TITLE} - {self.case['reference_code']} - {self.case['organisation']['name']}",
        }
        return super().get_context_data(*args, **context, **kwargs)


class CaseAssignmentAllocateToMe(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.CaseAssignmentsAllocateToMeForm

    def form_valid(self, form):
        data = form.cleaned_data
        self.allocate_to_me(data)
        messages.success(self.request, f"You have been successfully added as case adviser")
        self.queue_id = data["queue_id"]
        self.case_id = data["case_id"]

        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error allocating user as case advisor",
        "Unexpected error allocating you as case advisor",
    )
    def allocate_to_me(self, data):
        return put_queue_case_assignments(
            self.request, data["queue_id"], [data["case_id"]], [data["user_id"]], "Allocated self to the case"
        )
    
    def get_success_url(self):
        case = get_case(self.request, self.case_id)
        if case.case_type['sub_type']['key'] == 'f680_clearance':
            return reverse("cases:f680:details", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})
        
        return reverse("cases:case", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})

class CaseAssignmentsCaseOfficer(LoginRequiredMixin, CaseContextBasicMixin, SuccessMessageMixin, FormView):
    template_name = "core/form.html"
    form_class = forms.CaseAssignmentsCaseOfficerForm
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
        default_success_url = reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})
        return self.request.GET.get("return_to", default_success_url)

    def get_context_data(self, *args, **kwargs):
        context = {
            "back_link_url": reverse("queues:case_assignment_select_role", kwargs={"pk": self.kwargs["pk"]})
            + f"?{self.request.GET.urlencode()}",
            "title": f"{self.form_class.Layout.DOCUMENT_TITLE} - {self.case['reference_code']} - {self.case['organisation']['name']}",
        }
        return super().get_context_data(*args, **context, **kwargs)


class CaseAssignmentsCaseAssigneeSteps:
    SELECT_USERS = "SELECT_USERS"
    SELECT_QUEUE = "SELECT_QUEUE"


class CaseAssignmentsCaseAssignee(
    LoginRequiredMixin,
    CaseContextBasicMixin,
    BaseSessionWizardView,
):
    form_list = [
        (CaseAssignmentsCaseAssigneeSteps.SELECT_USERS, forms.CaseAssignmentUsersForm),
        (CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE, forms.CaseAssignmentQueueForm),
    ]

    condition_dict = {
        CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE: is_queue_in_url_system_queue,
    }

    def dispatch(self, request, *args, **kwargs):
        self.case_ids = self.get_case_ids()
        self.queue_id = self.get_queue_id()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        user_data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))
        kwargs["request"] = self.request
        if step == CaseAssignmentsCaseAssigneeSteps.SELECT_USERS:
            kwargs["team_id"] = user_data["user"]["team"]["id"]
            if is_queue_in_url_system_queue(self):
                kwargs["is_next_step"] = True
        if step == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE:
            kwargs["user_id"] = user_data["user_id"] = user_data["user"]["id"]
        return kwargs

    def get_success_url(self):
        default_success_url = reverse("queues:cases", kwargs={"queue_pk": self.queue_id})
        return self.request.GET.get("return_to", default_success_url)

    def get_back_link_url(self):
        default_back_url = reverse("queues:case_assignment_select_role", kwargs={"pk": self.queue_id})
        return self.request.GET.get("return_to", default_back_url)

    def get_case_ids(self):
        return self.request.GET.getlist("cases")

    def get_queue_id(self):
        return str(self.kwargs["pk"])

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)

        context["back_link_url"] = self.get_back_link_url()
        context["title"] = (
            f"{form.Layout.DOCUMENT_TITLE} - {self.case['reference_code']} - {self.case['organisation']['name']}"
        )

        return context

    @expect_status(
        HTTPStatus.OK,
        "Error updating case adviser on cases",
        "Unexpected error updating case adviser on cases",
    )
    def update_case_adviser(self, form_dict):
        queue_id = self.queue_id
        if is_queue_in_url_system_queue(self):
            queue_id = form_dict[CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE].cleaned_data["queue"]
        case_ids = self.case_ids
        note = form_dict[CaseAssignmentsCaseAssigneeSteps.SELECT_USERS].cleaned_data["note"]
        user_ids = form_dict[CaseAssignmentsCaseAssigneeSteps.SELECT_USERS].cleaned_data["users"]
        return put_queue_case_assignments(self.request, queue_id, case_ids, user_ids, note)

    def done(self, form_list, form_dict, **kwargs):
        self.update_case_adviser(form_dict)
        messages.success(self.request, f"Case adviser was added successfully")
        url = check_url(self.request, self.get_success_url())
        return redirect(url)
