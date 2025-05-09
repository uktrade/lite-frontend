from django.urls import reverse

from caseworker.cases.forms.create_ecju_query import new_ecju_query_form, ECJUQueryTypes
from caseworker.cases.services import get_case, post_ecju_query
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class NewECJUQueryView(LoginRequiredMixin, SingleFormView):
    # TODO: LTD-6084 - Replace this view/form with the django view/form used by F680s

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
