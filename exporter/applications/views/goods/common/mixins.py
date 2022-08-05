import requests

from django.http import Http404

from exporter.applications.services import get_application


class ApplicationMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.application = get_application(request, kwargs["pk"])
        except requests.exceptions.HTTPError:
            raise Http404(f"Couldn't get application {kwargs['pk']}")

        return super().dispatch(request, *args, **kwargs)
