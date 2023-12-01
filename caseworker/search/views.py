from django.views.generic import FormView
from django.urls import reverse_lazy
import json

from core.auth.views import LoginRequiredMixin

from .forms import ProductSearchForm
from .helpers import group_results_by_combination
from .services import get_product_search_results
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()

        # when we first get to the page query_params are empty.
        # if we don't use empty string then search term becomes None
        # and we get some results even though the input field is empty
        query_params = {
            "search": self.request.GET.get("search_string", ""),
            "page": self.request.GET.get("page", 1),
        }
        results = get_product_search_results(self.request, query_params)
        results = group_results_by_combination(results)
        context = super().get_context_data()
        context = {
            **context,
            "ALL_CASES_QUEUE_ID": ALL_CASES_QUEUE_ID,
            "customiser_spec": self.customiser_spec(),
            "search_results": results,
            "data": {
                "total_pages": results["count"] // form.page_size,
            },
        }
        return context

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
                    {"label": "Control entry", "key": "control_entry", "default_visible": True},
                    {"label": "Regime", "key": "regime", "default_visible": True},
                    {"label": "Report summary", "key": "report_summary", "default_visible": True},
                    {"label": "Assessment notes", "key": "assessment_notes", "default_visible": True},
                    {"label": "TAU assessor", "key": "tau_assessor", "default_visible": False},
                    {"label": "Quantity", "key": "quantity", "default_visible": False},
                    {"label": "Value", "key": "value", "default_visible": False},
                ],
            }
        )
