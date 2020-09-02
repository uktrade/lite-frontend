from http import HTTPStatus

from django.http import HttpResponse

from core import client
from core.helpers import convert_parameters_to_query_params
from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm
from exporter.core import constants


FILENAME = "OpenLicenceReturns.csv"


def get_compliance_list(request):
    data = client.get(request, f"/compliance/exporter/?page={request.GET.get('page', 1)}")
    return data.json()


def get_compliance_detail(request, pk):
    data = client.get(request, f"/compliance/exporter/{pk}/")
    return data.json()


def get_case_visit_reports(request, pk, page=1):
    querystring = convert_parameters_to_query_params({"pk": pk, "page": page})
    data = client.get(request, f"/compliance/exporter/{pk}/visits/{querystring}")
    return data.json()


def get_case_visit_report(request, pk):
    data = client.get(request, f"/compliance/exporter/visits/{pk}/")
    return data.json()


def get_open_licence_returns(request):
    page = request.GET.get("page", 1)
    data = client.get(request, f"/compliance/open-licence-returns/?page={page}")
    return data.json()


def get_open_licence_return_download(request, pk):
    data = client.get(request, f"/compliance/open-licence-returns/{pk}/")
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
    if request.FILES["file"].size > constants.MAX_OPEN_LICENCE_RETURNS_FILE_SIZE:
        return {"errors": {"file": [OpenReturnsForm.Upload.SIZE_ERROR]}}, HTTPStatus.BAD_REQUEST

    try:
        file = request.FILES.pop("file")[0]
        json["file"] = file.read().decode("utf-8")
    except Exception:  # noqa
        return {"errors": {"file": [OpenReturnsForm.Upload.READ_ERROR]}}, HTTPStatus.BAD_REQUEST

    data = client.post(request, "/compliance/open-licence-returns/", json)
    return data.json(), data.status_code
