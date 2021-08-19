from rest_framework import views
from rest_framework.response import Response

from django.shortcuts import redirect
from django.views.generic import FormView

from core.auth.permissions import IsAuthbrokerAuthenticated

from caseworker.auth.views import CaseworkerLoginRequiredMixin
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
            for name in ["search", "page"]:
                if form.cleaned_data[name]:
                    query_params[name] = form.cleaned_data[name]

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

    def get(self, request, *args, **kwargs):
        form = forms.AutocompleteForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
        else:
            q = ""
        results = self.service(request=request, q=q)
        return Response(results)


class ApplicationSearchView(AbstractSearchView, CaseworkerLoginRequiredMixin, FormView):
    template_name = "search/search-application.html"
    service = staticmethod(services.get_application_search_results)


class ApplicationAutocompleteView(AbstractAutocompleteView, views.APIView):
    service = staticmethod(services.get_application_autocomplete)


class ProductSearchView(AbstractSearchView, CaseworkerLoginRequiredMixin, FormView):
    template_name = "search/search-product.html"
    form_class = forms.SearchForm
    service = staticmethod(services.get_product_search_results)

    def get_context_data(self, **kwargs):
        return super().get_context_data(hide_page_numbers=True, **kwargs)


class ProductAutocompleteView(AbstractAutocompleteView, views.APIView):
    service = staticmethod(services.get_product_autocomplete)


class ProductDetailSpireView(CaseworkerLoginRequiredMixin, FormView):
    template_name = "search/product-details.html"
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        product = services.get_spire_product(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(product=product, **kwargs)

    def form_valid(self, form):
        services.create_spire_product_comment(
            request=self.request, pk=self.kwargs["pk"], data={"source": "SPIRE", "text": form.cleaned_data["text"]}
        )
        return redirect(self.request.get_full_path())


class ProductDetailLiteView(CaseworkerLoginRequiredMixin, FormView):
    template_name = "search/product-details.html"
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        product = services.get_lite_product(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(product=product, **kwargs)

    def form_valid(self, form):
        services.create_product_comment(
            request=self.request, pk=self.kwargs["pk"], data={"source": "LITE", "text": form.cleaned_data["text"]}
        )
        return redirect(self.request.get_full_path())
