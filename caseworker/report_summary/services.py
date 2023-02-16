from core import client
from urllib.parse import quote_plus


def _get_url(endpoint, search_term):
    query_string = f"?name={quote_plus(search_term)}" if search_term else ""
    return f"/static/report_summary/{endpoint}/{query_string}"


def get_report_summary_prefix(request, pk):
    response = client.get(request, f"/static/report_summary/prefixes/{pk}")
    response.raise_for_status()
    return response.json()


def get_report_summary_prefixes(request, search_term):
    response = client.get(request, _get_url("prefixes", search_term))
    return response.json()


def get_report_summary_subject(request, pk):
    response = client.get(request, f"/static/report_summary/subjects/{pk}")
    response.raise_for_status()
    return response.json()


def get_report_summary_subjects(request, search_term):
    response = client.get(request, _get_url("subjects", search_term))
    return response.json()
