from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin

from .helpers import group_results_by_cle
from .forms import ProductSearchForm
from .services import get_product_search_results
from ..core.constants import ALL_CASES_QUEUE_ID


class ProductSearchView(LoginRequiredMixin, FormView):
    template_name = "search/products.html"
    form_class = ProductSearchForm

    def form_valid(self, form):
        query_params = {
            "search": form.cleaned_data["search_string"],
            "page": form.cleaned_data["page"],
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
        return self.render_to_response(context)
