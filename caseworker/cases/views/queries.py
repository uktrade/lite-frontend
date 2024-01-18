from django.urls import reverse
from django.shortcuts import redirect

from django.views.generic import FormView

from caseworker.cases.forms.queries import CloseQuery
from caseworker.cases.services import put_ecju_query


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
