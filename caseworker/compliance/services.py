from django.http import HttpResponse

from core import client


FILENAME = "OpenLicenceReturns.csv"


def get_compliance_licences(request, case_id, reference, page):
    url = f"/compliance/{case_id}/licences/?reference={reference}&page={page}"
    data = client.get(request, url)
    return data.json()


def get_open_licence_return_download(request, pk):
    data = client.get(request, f"/compliance/open-licence-returns/{pk}/")
    open_licence_returns = data.json()
    response = HttpResponse("\n" + open_licence_returns["returns_data"], content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{open_licence_returns["year"]}{FILENAME}"'
    return response
