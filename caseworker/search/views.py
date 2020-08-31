from django.views.generic import FormView

from caseworker.search import forms
from caseworker.search.services import get_search_results


class SearchForm(FormView):
    form_class = forms.CasesSearchForm
    template_name = "search/search.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs["data"] = self.request.GET
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        query_params = form.cleaned_data if form.is_valid() else {}
        if "search_string" in query_params:
            query_params["search"] = query_params.pop("search_string")
        results = get_search_results(self.request, query_params)
        context["results"] = results
        context["data"] = {"total_pages": results["count"] // form.page_size}
        return context
