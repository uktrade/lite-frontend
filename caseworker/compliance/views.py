from django.views.generic import TemplateView

from caseworker.compliance.services import get_open_licence_return_download
from caseworker.auth.views import CaseworkerLoginRequiredMixin


class AnnualReturnsDownload(CaseworkerLoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        return get_open_licence_return_download(request, pk)
