from django.views.generic import TemplateView

from caseworker.compliance.services import get_open_licence_return_download

from core.auth.views import LoginRequiredMixin


class AnnualReturnsDownload(LoginRequiredMixin, TemplateView):
    def get(self, request, pk):
        return get_open_licence_return_download(request, pk)
