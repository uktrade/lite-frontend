import json
from http import HTTPStatus

from rest_framework import views
from rest_framework.response import Response

from django.views.generic import FormView
from django.urls import reverse_lazy

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

from .forms import ProductSearchForm, ProductSearchSuggestForm
from .helpers import group_results_by_combination
from .services import get_product_search_results, get_product_autocomplete
from ..core.constants import ALL_CASES_QUEUE_ID


class ProductSearchView(LoginRequiredMixin, FormView):
    form_class = ProductSearchForm
    template_name = "search/products.html"
    success_url = reverse_lazy("search:products")

    def get_initial(self):
        return {
            "search_string": self.request.GET.get("search_string", ""),
            "page": self.request.GET.get("page", 1),
        }

    def dispatch(self, request, *args, **kwargs):
        # when we first get to the page query_params are empty.
        # if we don't use empty string then search term becomes None
        # and we get some results even though the input field is empty
        query_params = {
            "search": self.request.GET.get("search_string", ""),
            "page": self.request.GET.get("page", 1),
        }
        self.results, status = get_product_search_results(self.request, query_params)

        if status not in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return error_page(self.request, getattr(self.results, "error", "An error occurred"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_pages = 1
        form = self.get_form()
        if "errors" not in self.results.keys():
            self.results = group_results_by_combination(self.results)
            total_pages = self.results["count"] // form.page_size
        return {
            **context,
            "ALL_CASES_QUEUE_ID": ALL_CASES_QUEUE_ID,
            "customiser_spec": self.customiser_spec(),
            "data": {"total_pages": total_pages},
            "search_results": self.results,
        }

    def customiser_spec(self) -> str:
        return json.dumps(
            {
                "options_label": "Customise search results",
                "identifier": "product-search-view",
                "analytics_prefix": "psv",
                "options_hint": "Select columns to show",
                "toggleable_elements": [
                    {"label": "Assessment date", "key": "assessment_date", "default_visible": True},
                    {"label": "Destination", "key": "destination", "default_visible": True},
                    {"label": "Control list entry", "key": "control_list_entry", "default_visible": True},
                    {"label": "Regime", "key": "regime", "default_visible": True},
                    {"label": "Report summary", "key": "report_summary", "default_visible": True},
                    {"label": "Assessment notes", "key": "assessment_notes", "default_visible": True},
                    {"label": "TAU assessor", "key": "tau_assessor", "default_visible": False},
                    {"label": "Quantity", "key": "quantity", "default_visible": False},
                    {"label": "Value", "key": "value", "default_visible": False},
                ],
            }
        )


class ProductSearchSuggestView(LoginRequiredMixin, views.APIView):
    def get(self, request):
        query = ""

        form = ProductSearchSuggestForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["q"]

        results = get_product_autocomplete(self.request, query)
        return Response(results)
