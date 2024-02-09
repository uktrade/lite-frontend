from django.http import Http404
from django.urls import reverse
from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.helpers.ecju_queries import get_ecju_queries
from caseworker.cases.services import put_ecju_query
from core.auth.views import LoginRequiredMixin


class CloseQueryView(LoginRequiredMixin, FormView):
    form_class = CloseQueryForm
    template_name = "case/close-query.html"

    def dispatch(self, request, *args, **kwargs):
        self.lite_user = request.lite_user
        return super().dispatch(request, *args, **kwargs)

    def get_prefix(self):
        self.prefix = str(self.kwargs["query_pk"])
        return self.prefix

    def form_valid(self, form):
        data = {
            "response": form.cleaned_data["reason_for_closing_query"],
            "responded_by_user": self.lite_user["id"],
        }
        put_ecju_query(request=self.request, pk=self.kwargs["pk"], query_pk=self.kwargs["query_pk"], json=data)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.kwargs["pk"],
                "tab": "ecju-queries",
            },
        )

    def get_query(self, open_ecju_queries):
        for query in open_ecju_queries:
            if query["id"] == str(self.kwargs["query_pk"]):
                return query
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        open_ecju_queries, _ = get_ecju_queries(self.request, self.kwargs["pk"])
        query = self.get_query(open_ecju_queries)
        if not query:
            raise Http404

        context["title"] = "Close query"
        context["query"] = query

        return context
