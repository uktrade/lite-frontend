from http import HTTPStatus

from django.http import HttpResponse

from conf.client import post, get
from conf.constants import (
    MAX_OPEN_LICENCE_RETURNS_FILE_SIZE,
    OPEN_LICENCE_RETURNS_URL,
    COMPLIANCE_EXPORTER_URL,
    VISIT_URL,
)
from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm


FILENAME = "OpenLicenceReturns.csv"


def get_compliance_list(request):
    data = get(request, COMPLIANCE_EXPORTER_URL + f"?page={request.GET.get('page', 1)}")
    return data.json()


def get_compliance_detail(request, pk):
    data = get(request, COMPLIANCE_EXPORTER_URL + str(pk) + "/")
    return data.json()


def get_case_visit_reports(request, pk):
    data = get(request, COMPLIANCE_EXPORTER_URL + str(pk) + "/" + VISIT_URL)
    return data.json()


def get_case_visit_report(request, pk):
    data = get(request, f"{COMPLIANCE_EXPORTER_URL}{VISIT_URL}{str(pk)}/")
    return data.json()


def get_open_licence_returns(request):
    data = get(request, OPEN_LICENCE_RETURNS_URL + f"?page={request.GET.get('page', 1)}")
    return data.json()


def get_open_licence_return_download(request, pk):
    data = get(request, OPEN_LICENCE_RETURNS_URL + str(pk) + "/")
    open_licence_returns = data.json()
    response = HttpResponse("\n" + open_licence_returns["returns_data"], content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{open_licence_returns["year"]}{FILENAME}"'
    return response


def post_open_licence_return(request, json):
    if not json.get("year"):
        return {"errors": {"year": [OpenReturnsForm.Year.ERROR]}}, HTTPStatus.BAD_REQUEST

    if len(request.FILES) == 0:
        return {"errors": {"file": [OpenReturnsForm.Upload.NO_FILE_ERROR]}}, HTTPStatus.BAD_REQUEST
    if len(request.FILES) != 1:
        return {"errors": {"file": [OpenReturnsForm.Upload.MULTIPLE_FILES_ERROR]}}, HTTPStatus.BAD_REQUEST
    if request.FILES["file"].size > MAX_OPEN_LICENCE_RETURNS_FILE_SIZE:
        return {"errors": {"file": [OpenReturnsForm.Upload.SIZE_ERROR]}}, HTTPStatus.BAD_REQUEST

    try:
        file = request.FILES.pop("file")[0]
        json["file"] = file.read().decode("utf-8")
    except Exception:  # noqa
        return {"errors": {"file": [OpenReturnsForm.Upload.READ_ERROR]}}, HTTPStatus.BAD_REQUEST

    data = post(request, OPEN_LICENCE_RETURNS_URL, json)
    return data.json(), data.status_code
