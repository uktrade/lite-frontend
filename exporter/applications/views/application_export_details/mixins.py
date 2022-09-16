from django.http import Http404
from django.conf import settings


class NonF680SecurityClassifiedFlagMixin:
    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)
