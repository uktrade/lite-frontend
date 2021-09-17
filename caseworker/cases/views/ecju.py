from django.urls import reverse

from caseworker.cases.forms.create_ecju_query import new_ecju_query_form, ECJUQueryTypes
from caseworker.cases.services import get_case, post_ecju_query
from lite_forms.views import SingleFormView
from django.views.generic import TemplateView


from caseworker.cases.forms.create_ecju_query import NewEcjuQueryFormCrispy
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


class NewECJUQueryViewCrispy(LoginRequiredMixin, TemplateView):
    template_name = "case/new_ecju_query.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NewEcjuQueryFormCrispy(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            print("Done")
            # .. save your model
            # .. redirect

        return super(TemplateView, self).render_to_response(context)
