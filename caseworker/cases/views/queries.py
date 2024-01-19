from django.urls import reverse
from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.services import put_ecju_query
from core.auth.views import LoginRequiredMixin

from lite_forms.generators import error_page


class CloseQueryView(LoginRequiredMixin, FormView):
    def dispatch(self, request, *args, **kwargs):
        self.lite_user = request.lite_user if request.lite_user else None
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return CloseQueryForm

    def get_prefix(self):
        self.prefix = str(self.kwargs["query_pk"])
        return self.prefix

    def form_valid(self, form):
        data = {
            "response": form.cleaned_data["reason_for_closing_query"],
            "responded_by_user": self.lite_user.get("id") if self.lite_user else None,
        }
        response, _ = put_ecju_query(
            request=self.request, pk=self.kwargs["pk"], query_pk=self.kwargs["query_pk"], json=data
        )
        if "errors" in response:
            description = response["errors"]
            return error_page(self.request, description=description)

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
