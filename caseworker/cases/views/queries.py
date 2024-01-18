from typing import Any
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQuery
from caseworker.cases.forms.create_ecju_query import new_ecju_query_form, ECJUQueryTypes
from caseworker.cases.services import get_case, post_ecju_query, put_ecju_query
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class NewECJUQueryView(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        query_type = request.GET.get("query_type", ECJUQueryTypes.ECJU_QUERY)
        self.object_pk = kwargs["pk"]
        self.context = {"case": get_case(request, self.object_pk)}
        self.form = new_ecju_query_form(kwargs["queue_pk"], self.object_pk, query_type)
        self.action = post_ecju_query
        self.success_message = "ECJU query sent successfully"
        self.success_url = reverse(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": "ecju-queries"}
        )


class CloseQueryView(FormView):
    form_class = CloseQuery

    def post(self, request, *args, **kwargs):
        self.queue_pk = kwargs["queue_pk"]
        self.pk = kwargs["pk"]
        self.query_pk = kwargs["query_pk"]

        # there are multiple forms on the page with different 'name' attributes
        # so this is used to prepare the form data before checking if it is valid
        form_data = {
            key.replace(f"_{str(self.query_pk)}", ""): value
            for key, value in request.POST.items()
            if key.startswith("reason_for_closing_query")
        }
        form = CloseQuery(form_data)
        if form.is_valid():
            body = {"response": form_data["reason_for_closing_query"]}
            put_ecju_query(request=request, pk=self.pk, query_pk=self.query_pk, json=body)

        return redirect(reverse("cases:case", kwargs={"queue_pk": self.queue_pk, "pk": self.pk, "tab": "ecju-queries"}))
