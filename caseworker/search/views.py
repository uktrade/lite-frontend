from django.views.generic import FormView
from django.urls import reverse_lazy

from core.auth.views import LoginRequiredMixin

from .forms import ProductSearchForm
from .helpers import group_results_by_cle
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
        results = group_results_by_cle(results)
        context = super().get_context_data()
        context = {
            **context,
            "ALL_CASES_QUEUE_ID": ALL_CASES_QUEUE_ID,
            "search_results": results,
            "data": {
                "total_pages": results["count"] // form.page_size,
            },
        }
        return context
