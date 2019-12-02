from conf.settings import env


def export_vars(request):
    data = {
        "SERVICE_NAME": "LITE",
        "GOV_UK_URL": "https://www.gov.uk",
        "FEEDBACK_URL": env("FEEDBACK_URL"),
        "INTERNAL_URL": env("INTERNAL_FRONTEND_URL"),
        "GOOGLE_ANALYTICS_KEY": env("GOOGLE_ANALYTICS_KEY"),
        "CURRENT_PATH": request.get_full_path(),
        "CURRENT_PATH_WITHOUT_PARAMS": request.get_full_path().split("?")[0].split("#")[0],
    }
    return data
