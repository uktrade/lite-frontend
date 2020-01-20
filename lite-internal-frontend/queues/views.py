from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from cases.forms.assign_users import assign_users_form
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView
from queues.forms import edit_queue_form, new_queue_form
from queues.helpers import get_assigned_users_from_cases
from queues.services import (
    get_queue,
    get_queues,
    post_queues,
    put_queue,
    put_queue_case_assignments,
    get_queue_case_assignments,
)
from users.services import get_gov_user


class QueuesList(TemplateView):
    def get(self, request, **kwargs):
        queues = get_queues(request)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            "queues": queues,
            "user_data": user_data,
        }
        return render(request, "queues/index.html", context)


class AddQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.form = new_queue_form()
        self.action = post_queues
        self.success_url = reverse_lazy("queues:queues")


class EditQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)["queue"]
        self.form = edit_queue_form()
        self.action = put_queue
        self.success_url = reverse_lazy("queues:queues")


class CaseAssignments(TemplateView):
    def get(self, request, **kwargs):
        """
        Assign users to cases
        """
        queue_id = str(kwargs["pk"])
        queue = get_queue(request, queue_id)
        case_assignments, _ = get_queue_case_assignments(request, queue_id)

        case_ids = request.GET.get("cases").split(",")
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        # If no cases have been selected, return an error page
        if not request.GET.get("cases"):
            return error_page(request, "Invalid case selection")

        # Get assigned users
        assigned_users = get_assigned_users_from_cases(case_ids, case_assignments["case_assignments"])
        return form_page(
            request,
            assign_users_form(request, user_data["user"]["team"]["id"], queue["queue"], len(case_ids) > 1),
            data={"users": assigned_users},
        )

    def post(self, request, **kwargs):
        """
        Update the queue's case assignments
        """
        queue_id = str(kwargs["pk"])
        queue = get_queue(request, queue_id)
        case_ids = request.GET.get("cases").split(",")
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        data = {"case_assignments": []}

        # Append case and users to case assignments
        for case_id in case_ids:
            data["case_assignments"].append({"case_id": case_id, "users": request.POST.getlist("users")})

        response, _ = put_queue_case_assignments(request, queue_id, data)
        if "errors" in response:
            return form_page(
                request,
                assign_users_form(request, user_data["user"]["team"]["id"], queue["queue"], len(case_ids) > 1),
                data=request.POST,
                errors=response["errors"],
            )

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse("cases:cases"))
