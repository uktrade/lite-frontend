from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.forms.assign_users import assign_users_form
from cases.helpers import get_updated_cases_banner_queue_id
from conf.constants import ALL_CASES_QUEUE_ID
from core.helpers import convert_dict_to_query_params
from lite_content.lite_internal_frontend.cases import CasesListPage
from lite_forms.components import HiddenField, FiltersBar, Option, AutocompleteInput, Checkboxes, Select
from lite_forms.generators import error_page, form_page
from lite_forms.helpers import conditional
from lite_forms.views import SingleFormView
from queues.forms import new_queue_form, edit_queue_form
from queues.services import (
    get_queues,
    get_cases_search_data,
    post_queues,
    get_queue,
    put_queue,
    get_queue_case_assignments,
    put_queue_case_assignments,
)
from users.services import get_gov_user


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue.
        """
        case_type = request.GET.get("case_type")
        status = request.GET.get("status")
        sort = request.GET.get("sort")
        queue_pk = kwargs.get("queue_pk") or request.user.default_queue
        case_officer = request.GET.get("case_officer")
        assigned_user = request.GET.get("assigned_user")
        hidden = request.GET.get("hidden")

        # Page parameters
        params = {"page": int(request.GET.get("page", 1))}
        if sort:
            params["sort"] = sort
        if status:
            params["status"] = status
        if case_type:
            params["case_type"] = case_type
        if case_officer:
            params["case_officer"] = case_officer
        if assigned_user:
            params["assigned_user"] = assigned_user
        if hidden:
            params["hidden"] = hidden

        data = get_cases_search_data(request, queue_pk, params)
        updated_cases_banner_queue_id = get_updated_cases_banner_queue_id(queue_pk, data["results"]["queues"])

        # Filter bar
        filters = data["results"]["filters"]
        statuses = [Option(option["key"], option["value"]) for option in filters["statuses"]]
        case_types = [Option(option["key"], option["value"]) for option in filters["case_types"]]
        gov_users = [Option(option["id"], option["full_name"]) for option in filters["gov_users"]]

        filters = FiltersBar(
            [
                conditional(queue_pk, HiddenField(name="queue_id", value=queue_pk)),
                Select(name="case_type", title=CasesListPage.Filters.CASE_TYPE, options=case_types),
                Select(name="status", title=CasesListPage.Filters.CASE_STATUS, options=statuses),
                AutocompleteInput(
                    name="case_officer",
                    title=CasesListPage.Filters.CASE_OFFICER,
                    options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
                ),
                AutocompleteInput(
                    name="assigned_user",
                    title=CasesListPage.Filters.ASSIGNED_USER,
                    options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
                ),
                conditional(
                    data["results"]["is_work_queue"],
                    Checkboxes(
                        name="hidden",
                        options=[Option("true", CasesListPage.Filters.HIDDEN)],
                        classes=["govuk-checkboxes--small"],
                    ),
                ),
            ]
        )

        context = {
            "data": data,
            "queue": data["results"]["queue"],
            "page": params.pop("page"),
            "params": params,
            "params_str": convert_dict_to_query_params(params),
            "updated_cases_banner_queue_id": updated_cases_banner_queue_id,
            "filters": filters,
            "is_all_cases_queue": queue_pk == ALL_CASES_QUEUE_ID,
        }

        return render(request, "queues/cases.html", context)

    def post(self, request, **kwargs):
        """ Assign users depending on what cases were selected. """
        return redirect(
            reverse("queues:case_assignments", kwargs={"pk": kwargs["queue_pk"]})
            + "?cases="
            + ",".join(request.POST.getlist("cases"))
        )


class QueuesList(TemplateView):
    def get(self, request, **kwargs):
        page = request.GET.get("page", 1)
        queues = get_queues(request, page=page, disable_pagination=False)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            "data": queues,
            "user_data": user_data,
        }
        return render(request, "queues/manage.html", context)


class AddQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.form = new_queue_form(request)
        self.action = post_queues
        self.success_url = reverse_lazy("queues:manage")


class EditQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)
        self.form = edit_queue_form(request, self.object_pk)
        self.action = put_queue
        self.success_url = reverse_lazy("queues:manage")


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
        assigned_users = [
            assignment["user"] for assignment in case_assignments["case_assignments"] if assignment["case"] in case_ids
        ]
        return form_page(
            request,
            assign_users_form(request, user_data["user"]["team"]["id"], queue, len(case_ids) > 1),
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

        # Any assignments not selected should be removed (hence clear_existing_assignments)
        data = {"case_assignments": [], "remove_existing_assignments": True}

        # Append case and users to case assignments
        for case_id in case_ids:
            data["case_assignments"].append({"case_id": case_id, "users": request.POST.getlist("users")})

        response, _ = put_queue_case_assignments(request, queue_id, data)
        if "errors" in response:
            return form_page(
                request,
                assign_users_form(request, user_data["user"]["team"]["id"], queue, len(case_ids) > 1),
                data=request.POST,
                errors=response["errors"],
            )

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse("queues:cases", kwargs={"queue_pk": queue_id}))
