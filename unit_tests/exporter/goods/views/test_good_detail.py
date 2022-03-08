import pytest

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
            "is_replica": False,
            "replica_description": "",
            "is_covered_by_firearm_act_section_one_two_or_five": "",
            "firearms_act_section": "",
            "section_certificate_missing": None,
            "section_certificate_missing_reason": "",
            "section_certificate_number": None,
            "section_certificate_date_of_expiry": None,
            "serial_numbers_available": None,
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
