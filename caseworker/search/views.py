from rest_framework import views
from rest_framework.response import Response

from django.views.generic import FormView, TemplateView

from core.auth.permissions import IsAuthbrokerAuthenticated
from core.auth.views import LoginRequiredMixin
from caseworker.search import forms, helpers, services


class AbstractSearchView:
    form_class = forms.SearchForm

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
        results = self.service(self.request, query_params)
        helpers.highlight_results(results=results["results"])
        context["results"] = results
        context["data"] = {"total_pages": results["count"] // form.page_size}
        return context


class AbstractAutocompleteView:
    authentication_classes = []
    permission_classes = [IsAuthbrokerAuthenticated]

    def perform_authentication(self, request):
        pass

    def get(self, request):
        form = forms.AutocompleteForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
        else:
            q = ""
        results = self.service(request=request, q=q)
        return Response(results)


class ApplicationSearchView(AbstractSearchView, LoginRequiredMixin, FormView):
    template_name = "search/search-application.html"
    service = staticmethod(services.get_application_search_results)


class ApplicationAutocompleteView(AbstractAutocompleteView, views.APIView):
    service = staticmethod(services.get_application_autocomplete)


class ProductSearchView(AbstractSearchView, LoginRequiredMixin, FormView):
    template_name = "search/search-product.html"
    service = staticmethod(services.get_product_search_results)

    def get_context_data(self, **kwargs):
        return super().get_context_data(hide_page_numbers=True, **kwargs)


class ProductAutocompleteView(AbstractAutocompleteView, views.APIView):
    service = staticmethod(services.get_product_autocomplete)


class ProductDetailSpireView(LoginRequiredMixin, TemplateView):
    template_name = "search/product-details.html"

    def get_context_data(self, **kwargs):
        product = services.get_spire_product(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(product=product, **kwargs)


class ProductDetailLiteView(LoginRequiredMixin, TemplateView):
    template_name = "search/product-details.html"

    def get_context_data(self, **kwargs):
        product = services.get_lite_product(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(product=product, **kwargs)
