from django.views.generic import TemplateView

from compliance.services import get_open_licence_return_download


class AnnualReturnsDownload(TemplateView):
    def get(self, request, pk):
        return get_open_licence_return_download(request, pk)
