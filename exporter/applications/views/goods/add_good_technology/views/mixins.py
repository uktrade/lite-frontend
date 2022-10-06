from django.http import Http404
from django.conf import settings


class NonFirearmsTechnologyFlagMixin:
    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_NON_FIREARMS_TECHNOLOGY_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)
