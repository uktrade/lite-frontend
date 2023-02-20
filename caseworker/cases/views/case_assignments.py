from http import HTTPStatus
import itertools

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView
from caseworker.cases.forms import case_assignment as forms

from caseworker.cases.services import delete_case_assignment
from caseworker.cases.services import get_case
from caseworker.cases.views.conditionals import is_queue_in_url_system_queue
from caseworker.queues.services import put_queue_case_assignments

from caseworker.users.services import get_gov_user


class CaseAssignmentRemove(LoginRequiredMixin, FormView):
    template_name = "case/remove-case-assignment.html"
    form_class = forms.CaseAssignmentRemove

    def _get_adviser(self, case, assignment_id):
        all_assigned_users = itertools.chain.from_iterable(
            [queue_users for queue_users in case["assigned_users"].values()]
        )
        assigned_users_by_assignment_id = {user["assignment_id"]: user for user in all_assigned_users}
        try:
            return assigned_users_by_assignment_id[assignment_id]
        except KeyError:
            raise Http404

    def _get_adviser_identifier(self, case, assignment_id):
        adviser = self._get_adviser(case, assignment_id)
        adviser_identifier = adviser["email"]
        if adviser["first_name"] and adviser["last_name"]:
            adviser_identifier = f"{adviser['first_name']} {adviser['last_name']}"
        return adviser_identifier

    def get_case(self):
        return get_case(self.request, self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        case = self.get_case()
        return super().get_context_data(
            case=case,
            queue_id=self.kwargs["queue_pk"],
            case_id=self.kwargs["pk"],
            adviser_identifier=self._get_adviser_identifier(case, self.request.GET.get("assignment_id")),
            **kwargs,
        )

    def get_success_url(self):
        return reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})

    def get_initial(self):
        return {"assignment_id": self.request.GET.get("assignment_id")}

    def form_valid(self, form):
        adviser_identifier = self._get_adviser_identifier(self.get_case(), form.cleaned_data["assignment_id"])
        response = delete_case_assignment(self.request, self.kwargs["pk"], form.cleaned_data["assignment_id"])
        if response.ok:
            messages.success(self.request, f"{adviser_identifier} was successfully removed as case adviser")
        else:
            messages.error(
                self.request,
                f"An error occurred when removing {adviser_identifier} as case adviser. Please try again later",
            )

        return super().form_valid(form)


SELECT_USERS = "SELECT_USERS"
SELECT_QUEUE = "SELECT_QUEUE"


class CaseAssignmentAddUser(
    LoginRequiredMixin,
    BaseSessionWizardView,
):
    form_list = [
        (SELECT_USERS, forms.CaseAssignmentUsersForm),
        (SELECT_QUEUE, forms.CaseAssignmentQueueForm),
    ]

    condition_dict = {
        SELECT_QUEUE: is_queue_in_url_system_queue,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        user_data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))
        kwargs["request"] = self.request
        if step == SELECT_USERS:
            kwargs["team_id"] = user_data["user"]["team"]["id"]
        if step == SELECT_QUEUE:
            kwargs["user_id"] = user_data["user_id"] = user_data["user"]["id"]
        return kwargs

    def get_success_url(self):
        return reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})

    def get_back_link_url(self):
        return reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)

        context["back_link_url"] = self.get_back_link_url()
        context["title"] = form.Layout.TITLE

        return context

    @expect_status(
        HTTPStatus.OK,
        "Error updating case adviser on cases",
        "Unexpected error updating case adviser on cases",
    )
    def update_case_adviser(self, form_dict):
        queue_id = self.kwargs["queue_pk"]
        if is_queue_in_url_system_queue(self):
            queue_id = form_dict[SELECT_QUEUE].cleaned_data["queue"]
        case_ids = [str(self.kwargs["pk"])]
        note = form_dict[SELECT_USERS].cleaned_data["note"]
        user_ids = form_dict[SELECT_USERS].cleaned_data["users"]
        return put_queue_case_assignments(self.request, queue_id, case_ids, user_ids, note)

    def done(self, form_list, form_dict, **kwargs):
        self.update_case_adviser(form_dict)
        messages.success(self.request, f"Case adviser was added successfully")
        return redirect(self.get_success_url())
