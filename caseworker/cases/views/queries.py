from http import HTTPStatus

from django.http import Http404
from django.urls import reverse
from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.helpers.ecju_queries import get_open_ecju_query, put_ecju_query
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status


class CloseQueryMixin:

    def get_prefix(self):
        self.prefix = str(self.kwargs["query_pk"])
        return self.prefix

    def form_valid(self, form):
        self.close_query(form.cleaned_data["reason_for_closing_query"])
        return super().form_valid(form)

    @expect_status(
        HTTPStatus.OK,
        "Error closing ECJU Query",
        "Unexpected error closing ECJU Query.",
    )
    def close_query(self, reason_for_closing_query):
        return put_ecju_query(self.request, self.kwargs["pk"], self.kwargs["query_pk"], reason_for_closing_query)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = get_open_ecju_query(self.request, self.kwargs["pk"], self.kwargs["query_pk"])
        if not query:
            raise Http404
        context["title"] = "Close query"
        context["query"] = query
        return context


class CloseQueryView(LoginRequiredMixin, CloseQueryMixin, FormView):
    form_class = CloseQueryForm
    template_name = "case/close-query.html"

    def get_success_url(self):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.kwargs["pk"],
                "tab": "ecju-queries",
            },
        )
