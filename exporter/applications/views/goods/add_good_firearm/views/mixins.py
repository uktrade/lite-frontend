from django.conf import settings
from django.http import Http404


class Product2FlagMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404("Feature flag not set")

        return super().dispatch(request, *args, **kwargs)
