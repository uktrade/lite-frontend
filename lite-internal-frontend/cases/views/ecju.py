from http import HTTPStatus

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.forms.create_ecju_query import (
    choose_ecju_query_type_form,
    create_ecju_query_write_or_edit_form,
    create_ecju_create_confirmation_form,
    choose_picklist_type_form,
)
from cases.services import get_ecju_queries, post_ecju_query, get_case
from cases.validators import validate_query_type_question
from lite_forms.components import Option, HiddenField
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView
from picklists.services import get_picklists, get_picklist_item


class ViewEcjuQueries(TemplateView):
    def _get_ecju_queries(self, request, case_id):
        ecju_queries = get_ecju_queries(request, case_id)[0]
        open_ecju_queries = list()
        closed_ecju_queries = list()
        for query in ecju_queries.get("ecju_queries"):
            if query.get("response"):
                closed_ecju_queries.append(query)
            else:
                open_ecju_queries.append(query)
        return open_ecju_queries, closed_ecju_queries

    def get(self, request, **kwargs):
        """
        Get all ECJU queries for the given case, divided into open and close
        """
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        open_ecju_queries, closed_ecju_queries = self._get_ecju_queries(request, case_id)
        context = {
            "case": case,
            "open_ecju_queries": open_ecju_queries,
            "closed_ecju_queries": closed_ecju_queries,
        }
        return render(request, "case/views/ecju-queries.html", context)


class ChooseECJUQueryType(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        picklist_type_choices = [
            Option("ecju_query", "Standard ECJU Query"),
            Option("pre_visit_questionnaire", "Pre-Visit Questionnaire Questions (ECJU Query)"),
            Option("compliance_actions", "Compliance Actions (ECJU Query)"),
        ]
        self.form = choose_picklist_type_form(
            picklist_type_choices, reverse("cases:ecju_queries", kwargs={"pk": str(kwargs["pk"])})
        )
        self.action = validate_query_type_question

    def get_success_url(self):
        return (
            reverse_lazy("cases:ecju_queries_add", kwargs={"pk": self.object_pk})
            + "?query_type="
            + self._validated_data.get("ecju_query_type")
        )


class CreateEcjuQuery(TemplateView):
    NEW_QUESTION_DDL_ID = "new_question"

    def get(self, request, **kwargs):
        """
        Show form for creating an ECJU query with a selection of template picklist questions
        """
        case_id = str(kwargs["pk"])
        query_type = request.GET.get("query_type")
        picklists = get_picklists(request, query_type, False)
        picklists = picklists.get("picklist_items")
        picklist_choices = [Option(self.NEW_QUESTION_DDL_ID, "Write a new question")] + [
            Option(picklist.get("id"), picklist.get("name")) for picklist in picklists
        ]
        form = choose_ecju_query_type_form(
            reverse("cases:choose_ecju_query_type", kwargs={"pk": case_id}), picklist_choices
        )

        return form_page(request, form, extra_data={"case_id": case_id}, data={"picklist": self.NEW_QUESTION_DDL_ID})

    def post(self, request, **kwargs):
        """
        Handle the different stages of the ECJU query forms and ultimately POST the query when confirmed
        """
        case_id = str(kwargs["pk"])
        form_name = request.POST.get("form_name")
        if form_name == "ecju_query_type_select":
            return self._handle_ecju_query_type_select_post(request, case_id)
        elif form_name == "ecju_query_write_or_edit_question":
            return self._handle_ecju_query_write_or_edit_post(case_id, request)
        elif form_name == "ecju_query_create_confirmation":
            return self._handle_ecju_query_confirmation_post(case_id, request)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(None, "We had an issue creating your question. Try again later.")

    def _handle_ecju_query_type_select_post(self, request, case_id):
        picklist_selection = request.POST.get("picklist")

        if picklist_selection != self.NEW_QUESTION_DDL_ID:
            picklist_item_text = get_picklist_item(request, picklist_selection)["text"]
        else:
            picklist_item_text = ""
        query_type = request.GET.get("query_type")
        form = create_ecju_query_write_or_edit_form(
            reverse("cases:ecju_queries_add", kwargs={"pk": case_id}) + "?query_type=" + query_type
        )
        data = {"question": picklist_item_text}

        return form_page(request, form, data=data)

    def _handle_ecju_query_write_or_edit_post(self, case_id, request):
        # Post the form data to API for validation only
        data = {
            "question": request.POST.get("question"),
            "query_type": request.GET.get("query_type"),
            "validate_only": True,
        }
        ecju_query, status_code = post_ecju_query(request, case_id, data)

        if status_code != 200:
            return self._handle_ecju_query_form_errors(case_id, ecju_query, request)
        else:
            form = create_ecju_create_confirmation_form()
            form.questions.append(HiddenField("question", request.POST.get("question")))
            return form_page(request, form)

    def _handle_ecju_query_confirmation_post(self, case_id, request):
        data = {
            "question": request.POST.get("question"),
            "query_type": request.GET.get("query_type"),
            "ecju_query_confirmation": "Yes",
        }

        confirmation = request.POST.get("ecju_query_confirmation")

        if confirmation:
            if confirmation.lower() == "yes":
                ecju_query, status_code = post_ecju_query(request, case_id, data)

                if status_code != HTTPStatus.CREATED:
                    return self._handle_ecju_query_form_errors(case_id, ecju_query, request)
                else:
                    return redirect(reverse("cases:ecju_queries", kwargs={"pk": case_id}))
            else:
                query_type = request.GET.get("query_type")
                form = create_ecju_query_write_or_edit_form(
                    reverse("cases:ecju_queries_add", kwargs={"pk": case_id}) + "?query_type=" + query_type
                )

            return form_page(request, form, data=data)
        else:
            errors = {"ecju_query_confirmation": ["This field is required"]}

            form = create_ecju_create_confirmation_form()
            form.questions.append(HiddenField("question", request.POST.get("question")))
            return form_page(request, form, errors=errors)

    def _handle_ecju_query_form_errors(self, case_id, ecju_query, request):
        errors = ecju_query.get("errors")
        errors = {error: message for error, message in errors.items()}
        query_type = request.GET.get("query_type")
        form = create_ecju_query_write_or_edit_form(
            reverse("cases:ecju_queries_add", kwargs={"pk": case_id}) + "?query_type=" + query_type
        )
        data = {"question": request.POST.get("question"), "query_type": request.GET.get("query_type")}
        return form_page(request, form, data=data, errors=errors)
