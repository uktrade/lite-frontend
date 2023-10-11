from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin

from .forms import ProductSearchForm
from .services import get_product_search_results


class ProductSearchView(LoginRequiredMixin, FormView):
    template_name = "search/products.html"
    form_class = ProductSearchForm

    def get_search_results(self, request, query):
        search_results = get_product_search_results(request, query)

        return search_results

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["search_results"] = self.get_search_results(self.request, self.request.GET)

        return context
