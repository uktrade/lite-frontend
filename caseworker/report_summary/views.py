from django.http import JsonResponse
from django.views.generic import TemplateView

from caseworker.report_summary.services import get_report_summary_prefixes
from core.auth.views import LoginRequiredMixin


class ReportSummaryPrefix(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        """
        Return JSON representation of prefixes for use in autocompletion
        """
        return JsonResponse(data=(get_report_summary_prefixes(request)))
