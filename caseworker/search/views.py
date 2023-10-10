from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin


class ProductSearchView(LoginRequiredMixin, TemplateView):
    template_name = "search/products.html"
