import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture(scope="function")
def good():
    return {
        "id": "e0a485d0-156e-4152-bec9-4798c9f2871e",
        "name": "Advanced automatic rifle",
        "description": "Newly developed rifle for research purposes",
        "control_list_entries": [],
        "part_number": "12345/XZ",
        "is_good_controlled": {"key": "False", "value": "No"},
        "is_pv_graded": {"key": "no", "value": "No"},
        "item_category": {"key": "group2_firearms", "value": "Firearms"},
        "is_military_use": None,
        "is_component": None,
        "uses_information_security": None,
        "modified_military_use_details": None,
        "component_details": None,
        "information_security_details": None,
        "pv_grading_details": None,
        "software_or_technology_details": None,
        "firearm_details": {
            "type": {"key": "firearms", "value": "Firearms"},
            "year_of_manufacture": 0,
            "calibre": "50mm",
            "is_sporting_shotgun": False,
            "is_replica": False,
            "replica_description": "",
            "is_covered_by_firearm_act_section_one_two_or_five": "",
            "firearms_act_section": "",
            "section_certificate_missing": None,
            "section_certificate_missing_reason": "",
            "section_certificate_number": None,
            "section_certificate_date_of_expiry": None,
            "has_identification_markings": None,
            "no_identification_markings_details": None,
            "has_proof_mark": None,
            "no_proof_mark_details": "",
            "is_deactivated": None,
            "is_deactivated_to_standard": None,
            "date_of_deactivation": None,
            "deactivation_standard": "",
            "deactivation_standard_other": "",
            "number_of_items": None,
            "serial_numbers": [],
        },
        "case_id": None,
        "documents": [],
        "is_document_available": False,
        "is_document_sensitive": None,
        "status": {"key": "draft", "value": "Draft"},
        "query": None,
        "case_officer": None,
        "case_status": None,
    }


@pytest.fixture(scope="session")
def organisation_documents():
    return [
        {
            "document": "812bd3ee-e045-4e38-bbcd-2632f9664b7e",
            "expiry_date": "2025-01-01",
            "document_type": "section-one-certificate",
            "organisation": "16091f44-cd03-4839-9505-613fb5f13686",
            "reference_code": "FR-SECTION1-12345",
        },
        {
            "document": "259c4538-e093-49bc-8e36-d8047a1bf852",
            "expiry_date": "2024-12-31",
            "document_type": "section-two-certificate",
            "organisation": "16091f44-cd03-4839-9505-613fb5f13686",
            "reference_code": "FR-SECTION2-12345",
        },
        {
            "document": "21b6e69f-d770-4eb3-99e9-69c65a8d338b",
            "expiry_date": "2025-05-05",
            "document_type": "section-five-certificate",
            "organisation": "16091f44-cd03-4839-9505-613fb5f13686",
            "reference_code": "FR-SECTION5-12345",
        },
        {
            "document": "2ef7deeb-d72e-4321-ad70-efd07c1a66f3",
            "expiry_date": "2025-03-31",
            "document_type": "rfd-certificate",
            "organisation": "16091f44-cd03-4839-9505-613fb5f13686",
            "reference_code": "FR-RFD-1234",
        },
    ]


def test_get_good_detail_doesnot_contain_application_specific_details(authorized_client, requests_mock, good):
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/"), json={"good": good})
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/documents/"), json={})

    url = reverse("goods:good_detail", kwargs={"pk": "e0a485d0-156e-4152-bec9-4798c9f2871e", "type": "case-notes"})
    response = authorized_client.get(url)
    assert response.status_code == 200
    response_html = response.content.decode("utf-8")
    assert ("Name" in response_html) == True
    assert ("Product type" in response_html) == True
    assert ("Controlled" in response_html) == True
    assert ("Year of manufacture" in response_html) == False
    assert ("Identification markings" in response_html) == False


def test_firearms_act_on_good_detail_page_section5_uploaded(authorized_client, requests_mock, good):
    """
    Test to ensure correct details for Section5 are shown when the form is uploaded by the user.

    This is usually the first instance where a product covered under section5 is added, there after
    the system remembers it for future products.
    """
    good["firearm_details"]["is_covered_by_firearm_act_section_one_two_or_five"] = "Yes"
    good["firearm_details"]["firearms_act_section"] = "firearms_act_section5"
    good["firearm_details"]["section_certificate_missing"] = False
    good["firearm_details"]["section_certificate_number"] = "FX123/45"
    good["firearm_details"]["section_certificate_date_of_expiry"] = "2025-12-31"
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/"), json={"good": good})
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/documents/"), json={})

    url = reverse("goods:good_detail", kwargs={"pk": "e0a485d0-156e-4152-bec9-4798c9f2871e", "type": "case-notes"})
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    section_details = soup.find(id="covered-by-firearms-act-value").text
    section_details = section_details.replace("\t", "").replace("\n", " ").strip().split("  ")
    covered_by_firearms_act = section_details[0]
    expiry_date = section_details[1].strip()
    certificate_number = section_details[2].strip()

    assert covered_by_firearms_act == "Yes"
    assert certificate_number == "Reference FX123/45"
    assert expiry_date == "Expires 31 December 2025"


def test_firearms_act_on_good_detail_page_section5_upload_is_skipped(
    authorized_client, requests_mock, good, organisation_documents
):
    """
    Test to ensure section5 details are still shown correctly when the upload is skipped

    This is the case when the system determines that there is a valid section5 for this organisation
    and skips the upload.
    """
    good["firearm_details"]["is_covered_by_firearm_act_section_one_two_or_five"] = "Yes"
    good["firearm_details"]["firearms_act_section"] = "firearms_act_section5"
    good["firearm_details"]["section_certificate_missing"] = False
    good["organisation_documents"] = organisation_documents
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/"), json={"good": good})
    requests_mock.get(client._build_absolute_uri("/goods/e0a485d0-156e-4152-bec9-4798c9f2871e/documents/"), json={})

    url = reverse("goods:good_detail", kwargs={"pk": "e0a485d0-156e-4152-bec9-4798c9f2871e", "type": "case-notes"})
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    section_details = soup.find(id="covered-by-firearms-act-value").text
    section_details = section_details.replace("\t", "").replace("\n", " ").strip().split("  ")
    covered_by_firearms_act = section_details[0]
    expiry_date = section_details[1].strip()
    certificate_number = section_details[2].strip()

    assert covered_by_firearms_act == "Yes"
    assert certificate_number == "Reference FR-SECTION5-12345"
    assert expiry_date == "Expires 5 May 2025"
