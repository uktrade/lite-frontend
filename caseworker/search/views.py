from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import View


class ProductSearchView(View):
    def get(self, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_SEARCH:
            raise Http404("No feature flag")

        return HttpResponse("OK")
