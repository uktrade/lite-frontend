import datetime
import pytest
import uuid

from django.urls import reverse
from django.utils import timezone

from core import client
from core.constants import (
    OrganisationDocumentType,
    SerialChoices,
)


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def mock_application_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    return requests_mock.get(url=url, json=application)


@pytest.fixture
def mock_refused_application_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    application = {
        **application,
        "status": {"key": "finalised", "value": "Finalised"},
        "licence": None,
        "appeal_deadline": timezone.localtime().isoformat(),
    }
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    return requests_mock.get(url=url, json=application)


@pytest.fixture
def mock_application_put(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    return requests_mock.put(url=url, json=application)


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Don't know",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "No firearm act section",
        }
    )
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
        "quantity": 3.0,
        "value": "16.32",
        "unit": {"key": "GRM", "value": "Gram(s)"},
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "I will alter it real good",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "I will onward incorporate",
        "is_component": {"value": "This is a modified component", "key": "yes_modified"},
        "modified_details": "modified component",
        "firearm_details": {
            "section_certificate_date_of_expiry": "2030-12-12",
            "section_certificate_number": "12345",
            "section_certificate_missing": False,
            "section_certificate_missing_reason": "",
            "is_made_before_1938": True,
            "year_of_manufacture": 1930,
            "is_deactivated": True,
            "date_of_deactivation": datetime.date(2007, 12, 12).isoformat(),
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Not deactivated",
            "serial_numbers_available": SerialChoices.NOT_AVAILABLE,
            "no_identification_markings_details": "No markings",
            "serial_numbers": ["111", "222", "333"],
            "number_of_items": 3.0,
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
def mock_good_on_application_put(requests_mock, good_on_application):
    url = f"/applications/good-on-application/{good_on_application['id']}/"
    return requests_mock.put(url, json={})


@pytest.fixture
def mock_regimes_get(requests_mock):
    url = client._build_absolute_uri(f"/static/regimes/entries/")
    return requests_mock.get(url=url, json={"regimes": [{"rating": "T1"}, {"rating": "T5"}]})


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
        "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
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
            "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
        }
    ]
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_without_rfd_document(application):
    return application


@pytest.fixture
def firearm_product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:firearm_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def complete_item_product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:complete_item_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def component_accessory_product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:component_accessory_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def material_product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:material_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def technology_product_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:technology_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def product_on_application_summary_url_factory(application, good_on_application):
    def product_on_application_summary_url(summary_type):
        url = reverse(
            f"applications:{summary_type.replace('-', '_')}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
            },
        )
        return url

    return product_on_application_summary_url


@pytest.fixture
def product_on_application_summary_url(product_on_application_summary_url_factory):
    return product_on_application_summary_url_factory("product-on-application-summary")


@pytest.fixture
def attach_product_on_application_summary_url(product_on_application_summary_url_factory):
    return product_on_application_summary_url_factory("attach-product-on-application-summary")


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


@pytest.fixture
def control_list_entries(requests_mock):
    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    matcher = requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})
    return matcher


@pytest.fixture
def complete_item_on_application_summary_url_factory(application, good_on_application):
    def complete_item_on_application_summary_url(summary_type):
        url = reverse(
            f"applications:{summary_type.replace('-', '_')}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
            },
        )
        return url

    return complete_item_on_application_summary_url


@pytest.fixture
def complete_item_on_application_summary_url(complete_item_on_application_summary_url_factory):
    return complete_item_on_application_summary_url_factory("complete_item-on-application-summary")


@pytest.fixture
def component_accessory_on_application_summary_url_factory(application, good_on_application):
    def component_accessory_on_application_summary_url(summary_type):
        url = reverse(
            f"applications:{summary_type.replace('-', '_')}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
            },
        )
        return url

    return component_accessory_on_application_summary_url


@pytest.fixture
def component_accessory_on_application_summary_url(component_accessory_on_application_summary_url_factory):
    return component_accessory_on_application_summary_url_factory("component-accessory-on-application-summary")


@pytest.fixture
def material_on_application_summary_url_factory(application, good_on_application):
    def material_on_application_summary_url(summary_type):
        url = reverse(
            f"applications:{summary_type.replace('-', '_')}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
            },
        )
        return url

    return material_on_application_summary_url


@pytest.fixture
def material_on_application_summary_url(material_on_application_summary_url_factory):
    return material_on_application_summary_url_factory("material-on-application-summary")


@pytest.fixture
def technology_on_application_summary_url_factory(application, good_on_application):
    def technology_on_application_summary_url(summary_type):
        url = reverse(
            f"applications:{summary_type.replace('-', '_')}",
            kwargs={
                "pk": application["id"],
                "good_on_application_pk": good_on_application["id"],
            },
        )
        return url

    return technology_on_application_summary_url


@pytest.fixture
def technology_on_application_summary_url(technology_on_application_summary_url_factory):
    return technology_on_application_summary_url_factory("technology-on-application-summary")
