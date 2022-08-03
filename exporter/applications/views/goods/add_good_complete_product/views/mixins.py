from django.http import Http404
from django.conf import settings


class NonFirearmsFlagMixin:
    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_NON_FIREARMS_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)
