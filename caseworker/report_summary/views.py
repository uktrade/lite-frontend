from django.http import JsonResponse
from django.views.generic import TemplateView

from caseworker.report_summary.services import get_report_summary_prefixes, get_report_summary_subjects
from core.auth.views import LoginRequiredMixin


class ReportSummaryPrefix(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        """
        Return JSON representation of prefixes for use in autocompletion
        """
        search_term = request.GET.get("name")
        prefixes = get_report_summary_prefixes(request)

        if search_term:
            filtered_prefixes = [
                prefix for prefix in prefixes["report_summary_prefixes"] if prefix["name"].startswith(search_term)
            ]
            return JsonResponse(data={"report_summary_prefixes": filtered_prefixes})

        return JsonResponse(data=prefixes)


class ReportSummarySubject(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        """
        Return JSON representation of prefixes for use in autocompletion
        """
        return JsonResponse(data=(get_report_summary_subjects(request)))
