from http import HTTPStatus

from django.urls import reverse
from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.services import put_ecju_query
from core.auth.views import LoginRequiredMixin
from core.exceptions import ServiceError


class CloseQueryView(LoginRequiredMixin, FormView):
    def dispatch(self, request, *args, **kwargs):
        self.lite_user = request.lite_user
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return CloseQueryForm

    def get_prefix(self):
        self.prefix = str(self.kwargs["query_pk"])
        return self.prefix

    def form_valid(self, form):
        data = {
            "response": form.cleaned_data["reason_for_closing_query"],
            "responded_by_user": self.lite_user["id"],
        }
        response, status_code = put_ecju_query(
            request=self.request, pk=self.kwargs["pk"], query_pk=self.kwargs["query_pk"], json=data
        )
        if status_code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
            message = response.get("errors", "An error occurred")
            raise ServiceError(
                message=message,
                status_code=status_code,
                response=response,
                log_message=message,
                user_message=message,
            )

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
