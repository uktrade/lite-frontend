from django.views.generic import FormView
from django.shortcuts import render

from caseworker.search import forms, services


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
        query_params = {}
        if form.is_valid():
            if form.cleaned_data["search_string"]:
                query_params["search"] = form.cleaned_data["search_string"]
            if form.cleaned_data["page"]:
                query_params["page"] = form.cleaned_data["page"]
            query_params.update(form.cleaned_data["filters"])
        results = services.get_search_results(self.request, query_params)

        context["results"] = results
        context["data"] = {"total_pages": results["count"] // form.page_size}
        return context
 

from rest_framework import permissions, views
from rest_framework.response import Response



class AutocompleteView(views.APIView):
    authentication_classes = []
    permission_classes = [
        permissions.AllowAny,
    ]

    def perform_authentication(self, request):
        pass

    def get(self, request):
        form = forms.AutocompleteForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
        else:
            q = ''
        results = services.get_autocomplete(request=request, q=q)
        return Response(results)
