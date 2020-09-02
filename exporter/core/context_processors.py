from exporter.core.constants import Permissions
from django.conf import settings


def export_vars(request):
    data = {
        "SERVICE_NAME": "LITE",
        "GOV_UK_URL": "https://www.gov.uk",
        "FEEDBACK_URL": settings.FEEDBACK_URL,
        "INTERNAL_URL": settings.INTERNAL_FRONTEND_URL,
        "GOOGLE_ANALYTICS_KEY": settings.GOOGLE_ANALYTICS_KEY,
        "CURRENT_PATH": request.get_full_path(),
        "CURRENT_PATH_WITHOUT_PARAMS": request.get_full_path().split("?")[0].split("#")[0],
        "USER_PERMISSIONS": Permissions,
        "AUTHBROKER_URL": settings.AUTHBROKER_URL,
    }
    return data
