from django.http import HttpResponse

from conf.client import get
from conf.constants import OPEN_LICENCE_RETURNS_URL, COMPLIANCE_URL, COMPLIANCE_LICENCES_URL

FILENAME = "OpenLicenceReturns.csv"


def get_compliance_licences(request, case_id, reference, page):
    data = get(request, COMPLIANCE_URL + case_id + COMPLIANCE_LICENCES_URL + f"?reference={reference}&page={page}",)
    return data.json()


def get_open_licence_return_download(request, pk):
    data = get(request, OPEN_LICENCE_RETURNS_URL + str(pk) + "/")
    open_licence_returns = data.json()
    response = HttpResponse("\n" + open_licence_returns["returns_data"], content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{open_licence_returns["year"]}{FILENAME}"'
    return response
