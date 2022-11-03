import requests

from django.conf import settings
from django.http import Http404

from exporter.applications.services import get_application
from exporter.goods.services import get_good, get_good_on_application


class NonFirearmsFlagMixin:
    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_NON_FIREARMS_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)


class GoodOnApplicationMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.good_on_application = get_good_on_application(request, kwargs["good_on_application_pk"])
        except requests.exceptions.HTTPError:
            raise Http404(f"Couldn't get good on application {kwargs['good_on_application_pk']}")

        good_id = self.good_on_application["good"]["id"]

        try:
            self.good = get_good(request, good_id, full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404(f"Couldn't get good {good_id}")

        return super().dispatch(request, *args, **kwargs)


class GoodMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.good = get_good(request, kwargs["good_pk"], full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404(f"Couldn't get good {kwargs['good_pk']}")

        return super().dispatch(request, *args, **kwargs)


class ApplicationMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.application = get_application(request, kwargs["pk"])
        except requests.exceptions.HTTPError:
            raise Http404(f"Couldn't get application {kwargs['pk']}")

        return super().dispatch(request, *args, **kwargs)
