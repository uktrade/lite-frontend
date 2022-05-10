import datetime
import pytest
import uuid

from django.urls import reverse

from core import client
from exporter.goods.forms.firearms import FirearmSerialIdentificationMarkingsForm


@pytest.fixture
def good_id(data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    return good["id"]


@pytest.fixture
def mock_application_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    yield requests_mock.get(url=url, json=application)


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"]["is_pv_graded"] = {"key": "yes", "value": "Yes"}
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_good_put(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/')
    return requests_mock.put(url=url, json={})


@pytest.fixture
def good_on_application(data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]

    return {
        "id": str(uuid.uuid4()),
        "good": good["good"],
        "quantity": 3,
        "value": "16.32",
        "firearm_details": {
            "section_certificate_date_of_expiry": "2030-12-12",
            "section_certificate_number": "12345",
            "section_certificate_missing": False,
            "section_certificate_missing_reason": "",
            "is_made_before_1938": True,
            "year_of_manufacture": 1930,
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "I will alter it real good",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "I will onward incorporate",
            "is_deactivated": True,
            "date_of_deactivation": datetime.date(2007, 12, 12).isoformat(),
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Not deactivated",
            "serial_numbers_available": FirearmSerialIdentificationMarkingsForm.SerialChoices.NOT_AVAILABLE,
            "no_identification_markings_details": "No markings",
            "serial_numbers": ["111", "222", "333"],
        },
    }


@pytest.fixture
def mock_good_on_application_post(requests_mock, data_standard_case, good_on_application):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/goods/')
    return requests_mock.post(url=url, json=good_on_application, status_code=201)


@pytest.fixture
def mock_good_on_application_get(requests_mock, good_on_application):
    url = client._build_absolute_uri(f'/applications/good-on-application/{good_on_application["id"]}')
    return requests_mock.get(url=url, json=good_on_application, status_code=200)


@pytest.fixture
def mock_control_list_entries_get(requests_mock):
    url = client._build_absolute_uri(f"/static/control-list-entries/")
    return requests_mock.get(url=url, json={"control_list_entries": [{"rating": "ML1a"}, {"rating": "ML22b"}]})


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


@pytest.fixture
def mock_good_document_post(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/')
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def mock_good_document_put(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    document_pk = good["documents"][0]["id"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/{document_pk}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture
def mock_good_document_delete(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    document_pk = good["documents"][0]["id"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/{document_pk}/')
    yield requests_mock.delete(url=url, json={})


@pytest.fixture
def organisation_id():
    return str(uuid.uuid4())


@pytest.fixture
def rfd_certificate(organisation_id):
    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    return {
        "id": str(uuid.uuid4()),
        "document": {
            "name": "rfd_certificate.txt",
            "s3_key": "rfd_certificate.txt.s3_key",
            "safe": True,
            "size": 3,
            "id": str(uuid.uuid4()),
        },
        "document_type": "rfd-certificate",
        "is_expired": False,
        "organisation": organisation_id,
        "expiry_date": expiry_date.strftime("%d %B %Y"),
        "reference_code": "RFD123",
    }


@pytest.fixture
def section_5_document(organisation_id):
    return {
        "id": str(uuid.uuid4()),
        "document": {
            "name": "section5.txt",
            "s3_key": "section5.txt.s3_key",
            "safe": True,
            "size": 3,
        },
        "document_type": "section-five-certificate",
        "is_expired": False,
        "organisation": organisation_id,
        "reference_code": "section 5 ref",
        "expiry_date": "30 September 2024",
    }


@pytest.fixture
def application(data_standard_case, requests_mock):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    matcher = requests_mock.get(url=app_url, json=data_standard_case["case"])
    return matcher


@pytest.fixture
def application_with_organisation_rfd_document(data_standard_case, requests_mock, rfd_certificate):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [rfd_certificate],
    }
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_with_organisation_and_application_rfd_document(data_standard_case, requests_mock, rfd_certificate):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [rfd_certificate],
    }
    case["additional_documents"] = [
        {
            "document_type": "rfd-certificate",
        }
    ]
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_without_rfd_document(application):
    return application


@pytest.fixture
def product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def application_with_rfd_and_section_5_document(data_standard_case, requests_mock, rfd_certificate, section_5_document):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [
            rfd_certificate,
            section_5_document,
        ],
    }
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher
