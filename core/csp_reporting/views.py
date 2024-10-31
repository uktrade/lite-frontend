import json
import sentry_sdk
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class CspReportView:
    @csrf_exempt
    def csp_report(request):
        if request.method == "POST":
            report = json.loads(request.body.decode("utf-8"))
            sentry_sdk.capture_message("CSP Violation", level="warning", extra=report)
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "method not allowed"}, status=405)
