import pytest

from exporter.goods import helpers


class DummyRequest:
    session = {"rfd_certificate": None}


@pytest.mark.parametrize(
    "serializer,json,serialized",
    [
        (
            helpers.add_section_certificate_details,
            {
                "firearm_details": {},
                "section_certificate_step": True,
                "is_covered_by_firearm_act_section_one_two_or_five": True,
                "firearms_act_section": "firearms_act_section1",
            },
            {
                "is_covered_by_firearm_act_section_one_two_or_five": True,
                "firearms_act_section": "firearms_act_section1",
            },
        ),
        (
            helpers.add_section_certificate_details,
            {
                "firearm_details": {},
                "firearms_certificate_uploaded": True,
                "section_certificate_number": "1234",
                "section_certificate_date_of_expiryday": "1",
                "section_certificate_date_of_expirymonth": "1",
                "section_certificate_date_of_expiryyear": "2023",
                "section_certificate_missing": False,
            },
            {
                "section_certificate_number": "1234",
                "section_certificate_date_of_expiry": "2023-01-01",
                "section_certificate_missing": False,
                "section_certificate_missing_reason": "",
            },
        ),
        (
            helpers.add_section_certificate_details,
            {
                "firearm_details": {},
                "firearms_certificate_uploaded": True,
                "section_certificate_missing": True,
                "section_certificate_missing_reason": "Lorem ipsum",
            },
            {
                "section_certificate_missing": True,
                "section_certificate_number": "",
                "section_certificate_missing_reason": "Lorem ipsum",
            },
        ),
        (
            helpers.add_identification_marking_details,
            {
                "firearm_details": {},
                "number_of_items_step": True,
                "number_of_items": 2,
                "identification_markings_step": True,
                "has_identification_markings": True,
                "no_identification_markings_details": "",
                "capture_serial_numbers_step": True,
                "serial_number_input_0": "1234",
                "serial_number_input_1": "5678",
            },
            {
                "has_identification_markings": True,
                "no_identification_markings_details": "",
                "number_of_items": 2,
                "serial_numbers": ["1234", "5678"],
            },
        ),
        (
            helpers.add_rfd_certificate_details,
            {
                "firearm_details": {},
                "firearms_dealer_certificate_step": True,
                "expiry_date_day": "1",
                "expiry_date_month": "1",
                "expiry_date_year": "2023",
                "reference_code": "12345",
            },
            {
                "document_on_organisation": {
                    "expiry_date": "2023-01-01",
                    "reference_code": "12345",
                    "document_type": "rfd-certificate",
                    "document": None,
                }
            },
        ),
        (
            helpers.add_rfd_details,
            {"firearm_details": {"is_covered_by_firearm_act_section_one_two_or_five": True,},},
            {"is_covered_by_firearm_act_section_one_two_or_five": True, "is_registered_firearm_dealer": False,},
        ),
        (
            helpers.add_rfd_details,
            {"firearm_details": {}, "registered_firearm_dealer_step": True, "is_registered_firearm_dealer": True,},
            {"is_registered_firearm_dealer": True,},
        ),
        (
            helpers.add_sporting_shotgun_details,
            {"firearm_details": {}, "sporting_shotgun_step": True, "is_sporting_shotgun": True, "type": "firearms",},
            {"is_sporting_shotgun": True, "type": "firearms",},
        ),
        (
            helpers.add_sporting_shotgun_details,
            {"firearm_details": {"is_registered_firearm_dealer": True,}, "type": "firearms",},
            {"is_registered_firearm_dealer": True, "is_sporting_shotgun": False,},
        ),
        (
            helpers.add_year_of_manufacture_details,
            {"firearm_details": {}, "firearm_year_of_manufacture_step": True, "year_of_manufacture": 2020,},
            {"year_of_manufacture": 2020,},
        ),
        (
            helpers.add_year_of_manufacture_details,
            {"firearm_details": {}, "firearm_year_of_manufacture_step": True, "year_of_manufacture": "",},
            {"year_of_manufacture": None,},
        ),
        (
            helpers.add_year_of_manufacture_details,
            {"firearm_details": {"is_registered_firearm_dealer": True,},},
            {"is_registered_firearm_dealer": True, "year_of_manufacture": 0,},
        ),
        (
            helpers.add_replica_details,
            {
                "firearm_details": {},
                "is_replica_step": True,
                "type": "firearms",
                "is_replica": True,
                "replica_description": "Lorem ipsum",
            },
            {"type": "firearms", "is_replica": True, "replica_description": "Lorem ipsum",},
        ),
        (
            helpers.add_calibre_details,
            {"firearm_details": {}, "firearm_calibre_step": True, "calibre": ".15 ACP",},
            {"calibre": ".15 ACP",},
        ),
        (
            helpers.add_calibre_details,
            {"firearm_details": {}, "firearm_calibre_step": True, "calibre": "",},
            {"calibre": None,},
        ),
        (
            helpers.add_product_type,
            {"firearm_details": {}, "product_type_step": True, "type": "firearms",},
            {"type": "firearms",},
        ),
    ],
)
def test_firearms_details_serializers(serializer, json, serialized):
    firearm_details = json["firearm_details"]

    if serializer == helpers.add_rfd_certificate_details:
        serializer(firearm_details, json, DummyRequest())
    else:
        serializer(firearm_details, json)
    assert json["firearm_details"] == serialized


def test_add_firearm_details_to_data():
    json = {
        "date_of_deactivation": "Lorem ipsum",
        "has_proof_mark": "Lorem ipsum",
        "no_proof_mark_details": "Lorem ipsum",
        "is_deactivated": "Lorem ipsum",
        "deactivation_standard": "Lorem ipsum",
        "deactivation_standard_other": "Lorem ipsum",
        "is_deactivated_to_standard": "Lorem ipsum",
    }
    expected = {
        "firearm_details": {
            "date_of_deactivation": "Lorem ipsum",
            "has_proof_mark": "Lorem ipsum",
            "no_proof_mark_details": "Lorem ipsum",
            "is_deactivated": "Lorem ipsum",
            "deactivation_standard": "Lorem ipsum",
            "deactivation_standard_other": "Lorem ipsum",
            "is_deactivated_to_standard": "Lorem ipsum",
        }
    }
    assert helpers.add_firearm_details_to_data(DummyRequest(), json) == expected
