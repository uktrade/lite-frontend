from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from .services import get_product_search_results


class ProductSearchView(LoginRequiredMixin, TemplateView):
    template_name = "search/products.html"

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_SEARCH:
            raise Http404("No feature flag")

        return super().dispatch(request, *args, **kwargs)

    def get_search_results(self, request, query):
        search_results = get_product_search_results(request, query)

        return search_results

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["search_results"] = self.get_search_results(self.request, self.request.GET)

        return context
