from core import client


def get_report_summary_prefixes(request):
    response = client.get(request, "/static/report_summary/prefixes/")
    return response.json()


def get_report_summary_subjects(request):
    response = client.get(request, "/static/report_summary/subjects/")
    return response.json()
