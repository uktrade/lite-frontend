import re

import pytest

from urllib import parse

from django.conf import settings
from django.test import Client

from core import client
from core.helpers import convert_value_to_query_param


application_id = "094eed9a-23cc-478a-92ad-9a05ac17fad0"
second_application_id = "08e69b60-8fbd-4111-b6ae-096b565fe4ea"
gov_uk_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"


@pytest.fixture
def data_case():
    return {
        "case": {
            "id": application_id,
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000001",
                "reference": {"key": "oiel", "value": "Open Individual Export Licence"},
                "type": {"key": "application", "value": "Application"},
                "sub_type": {"key": "open", "value": "Open Licence"},
            },
            "flags": [
                {
                    "id": "00000000-0000-0000-0000-000000000007",
                    "name": "Firearms",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                },
                {
                    "id": "00000000-0000-0000-0000-000000000014",
                    "name": "Enforcement Check Req",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                },
            ],
            "queues": ["0149b643-d38a-4d1a-b259-7f73ff4f7b97"],
            "queue_names": ["queue 20200629162022"],
            "assigned_users": {},
            "has_advice": {"user": False, "my_user": False, "team": False, "my_team": False, "final": False},
            "advice": [],
            "all_flags": [
                {"name": "Item not verified", "label": None, "colour": "default", "priority": 0, "level": "Good"},
                {
                    "name": "Destination20200629144727",
                    "label": "Test label",
                    "colour": "blue",
                    "priority": 0,
                    "level": "Destination",
                },
                {"name": "Enforcement Check Req", "label": None, "colour": "default", "priority": 0, "level": "Case"},
                {"name": "Firearms", "label": None, "colour": "default", "priority": 0, "level": "Case"},
                {
                    "name": "Organisation2020062916081",
                    "label": "Test label",
                    "colour": "pink",
                    "priority": 0,
                    "level": "Organisation",
                },
            ],
            "case_officer": None,
            "audit_notification": None,
            "reference_code": "GBOIEL/2020/0000045/P",
            "copy_of": None,
            "sla_days": 0,
            "sla_remaining_days": 60,
            "data": {
                "id": application_id,
                "name": "aggregate proactive architectures",
                "organisation": {
                    "id": "9bc26604-35ee-4383-9f58-74f8cab67443",
                    "primary_site": {
                        "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                        "name": "Headquarters",
                        "address": {
                            "id": "3f611bdb-ee89-41b5-a6f0-26f8b1182016",
                            "address_line_1": "42 Question Road",
                            "address_line_2": "",
                            "city": "London",
                            "region": "London",
                            "postcode": "Islington",
                            "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        },
                        "records_located_at": {
                            "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                            "name": "Headquarters",
                            "address": {
                                "address_line_1": "42 Question Road",
                                "address_line_2": "",
                                "region": "London",
                                "postcode": "Islington",
                                "city": "London",
                                "country": {"name": "United Kingdom"},
                            },
                        },
                    },
                    "type": {"key": "commercial", "value": "Commercial Organisation"},
                    "flags": [
                        {
                            "id": "25d7b462-0066-4a7d-bd7d-a9b0122fae09",
                            "name": "Organisation2020062916081",
                            "colour": "pink",
                            "label": "Test label",
                            "priority": 0,
                        }
                    ],
                    "status": {"key": "active", "value": "Active"},
                    "created_at": "2020-06-29T09:30:58.425994Z",
                    "updated_at": "2020-06-29T09:30:58.429528Z",
                    "name": "Archway Communications",
                    "eori_number": "1234567890AAA",
                    "sic_number": "2345",
                    "vat_number": "GB123456789",
                    "registration_number": "09876543",
                },
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "reference": {"key": "oiel", "value": "Open Individual Export Licence"},
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "open", "value": "Open Licence"},
                },
                "export_type": {"key": "permanent", "value": "Permanent"},
                "created_at": "2020-08-03T12:52:34.255494Z",
                "updated_at": "2020-08-03T12:52:37.708891Z",
                "submitted_at": "2020-08-03T12:52:37.703607Z",
                "submitted_by": "Automated Test",
                "status": {"key": "submitted", "value": "Submitted"},
                "case": application_id,
                "reference_code": "GBOIEL/2020/0000045/P",
                "is_major_editable": False,
                "goods_locations": {
                    "type": "sites",
                    "data": [
                        {
                            "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                            "name": "Headquarters",
                            "address": {
                                "id": "3f611bdb-ee89-41b5-a6f0-26f8b1182016",
                                "address_line_1": "42 Question Road",
                                "address_line_2": "",
                                "city": "London",
                                "region": "London",
                                "postcode": "Islington",
                                "country": {
                                    "id": "GB",
                                    "name": "United Kingdom",
                                    "type": "gov.uk Country",
                                    "is_eu": True,
                                },
                            },
                            "records_located_at": {
                                "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                                "name": "Headquarters",
                                "address": {
                                    "address_line_1": "42 Question Road",
                                    "address_line_2": "",
                                    "region": "London",
                                    "postcode": "Islington",
                                    "city": "London",
                                    "country": {"name": "United Kingdom"},
                                },
                            },
                        }
                    ],
                },
                "case_officer": None,
                "end_user": None,
                "ultimate_end_users": [
                    {
                        "id": "87fd61c4-ae4e-45c8-b635-40bd893e93d3",
                        "name": "Mary Example",
                        "address": "123 Fakse street",
                        "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        "website": "https://example.com/",
                        "type": "ultimate_end_user",
                        "organisation": "9bc26604-35ee-4383-9f58-74f8cab67443",
                        "document": {
                            "created_at": "2020-08-03T12:52:34.775Z",
                            "updated_at": "2020-08-03T12:52:37.396Z",
                            "id": "cd8d932a-ee7f-4162-9f74-4b614e1a285b",
                            "name": "Party document",
                            "s3_key": "lite-e2e-test-file.txt",
                            "size": None,
                            "virus_scanned_at": "2020-08-03T12:52:37.396Z",
                            "safe": True,
                            "document_ptr_id": "cd8d932a-ee7f-4162-9f74-4b614e1a285b",
                            "party_id": "87fd61c4-ae4e-45c8-b635-40bd893e93d3",
                        },
                        "sub_type": {"key": "commercial", "value": "Commercial Organisation"},
                        "role": {"key": "other", "value": "Other"},
                        "flags": [],
                        "copy_of": None,
                        "deleted_at": None,
                        "clearance_level": None,
                        "descriptors": None,
                    }
                ],
                "third_parties": [],
                "consignee": None,
                "inactive_parties": [],
                "activity": "Trading",
                "usage": None,
                "goods_types": [
                    {
                        "id": "3461adb9-0cc1-4097-b663-e06ac06198a2",
                        "description": "tool to assist peasants seize the means of production",
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "is_good_incorporated": True,
                        "control_list_entries": [{"rating": "ML1a", "text": "Outmoded bourgeois reactionaries"}],
                        "countries": [{"id": "US", "name": "United States", "type": "gov.uk Country", "is_eu": False}],
                        "document": None,
                        "flags": [
                            {
                                "id": "00000000-0000-0000-0000-000000000004",
                                "name": "Item not verified",
                                "colour": "default",
                                "label": None,
                            }
                        ],
                        "comment": None,
                        "report_summary": None,
                    }
                ],
                "additional_documents": [
                    {
                        "id": "bd95f6a1-24ea-4f98-8190-649d4189e612",
                        "created_at": "2020-08-03T12:52:35.345826Z",
                        "updated_at": "2020-08-03T12:52:37.462645Z",
                        "name": "judge farmers on political purity instead of horticultural ability.",
                        "s3_key": "lite-e2e-test-file.txt",
                        "size": None,
                        "virus_scanned_at": "2020-08-03T12:52:37.462286Z",
                        "safe": True,
                        "description": "this is a test additional document",
                        "application": application_id,
                    }
                ],
                "is_military_end_use_controls": False,
                "military_end_use_controls_ref": None,
                "is_informed_wmd": False,
                "informed_wmd_ref": None,
                "is_suspected_wmd": False,
                "suspected_wmd_ref": None,
                "intended_end_use": "intended end use",
                "licence": {"start_date": None, "duration": None, "status": None},
                "is_shipped_waybill_or_lading": True,
                "non_waybill_or_lading_route_details": None,
                "temp_export_details": None,
                "is_temp_direct_control": None,
                "temp_direct_control_details": None,
                "proposed_return_date": None,
                "trade_control_activity": {"key": None, "value": None},
                "trade_control_product_categories": [],
                "goodstype_category": {"key": "military", "value": "Military or dual use"},
                "contains_firearm_goods": True,
                "destinations": {
                    "type": "countries",
                    "data": [
                        {
                            "id": "cef005ab-9081-4669-9396-585160bd06db",
                            "country": {
                                "id": "US",
                                "name": "United States",
                                "flags": [
                                    {
                                        "colour": "blue",
                                        "name": "Destination20200629144727",
                                        "label": "Test label",
                                        "id": "a25d23e5-e0e0-4245-a611-d546edb140f8",
                                    }
                                ],
                            },
                            "flags": [],
                            "contract_types": ["aircraft_manufacturers", "air_force"],
                            "other_contract_type_text": None,
                        }
                    ],
                },
            },
            "next_review_date": None,
            "licences": [],
        }
    }


@pytest.fixture
def data_second_case(data_case):
    case = {**data_case}
    case["case"]["id"] = second_application_id
    return case


@pytest.fixture
def data_case_types():
    return [
        {"key": "oiel", "value": "Open Individual Export Licence"},
        {"key": "ogel", "value": "Open General Export Licence"},
        {"key": "oicl", "value": "Open Individual Trade Control Licence"},
        {"key": "siel", "value": "Standard Individual Export Licence"},
        {"key": "sicl", "value": "Standard Individual Trade Control Licence"},
        {"key": "sitl", "value": "Standard Individual Transhipment Licence"},
        {"key": "f680", "value": "MOD F680 Clearance"},
        {"key": "exhc", "value": "MOD Exhibition Clearance"},
        {"key": "gift", "value": "MOD Gifting Clearance"},
        {"key": "cre", "value": "HMRC Query"},
        {"key": "gqy", "value": "Goods Query"},
        {"key": "eua", "value": "End User Advisory Query"},
        {"key": "ogtcl", "value": "Open General Trade Control Licence"},
        {"key": "ogtl", "value": "Open General Transhipment Licence"},
        {"key": "comp_c", "value": "Compliance Site Case"},
        {"key": "comp_v", "value": "Compliance Visit Case"},
    ]


@pytest.fixture
def data_countries():
    return {'countries': [
        {'id': 'AE-AZ', 'name': 'Abu Dhabi', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AF', 'name': 'Afghanistan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AE-AJ', 'name': 'Ajman', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'XQZ', 'name': 'Akrotiri', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AX', 'name': 'Åland Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AL', 'name': 'Albania', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'DZ', 'name': 'Algeria', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AS', 'name': 'American Samoa', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AD', 'name': 'Andorra', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AO', 'name': 'Angola', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AI', 'name': 'Anguilla', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AQ', 'name': 'Antarctica', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AG', 'name': 'Antigua and Barbuda', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AR', 'name': 'Argentina', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AM', 'name': 'Armenia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AW', 'name': 'Aruba', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SH-AC', 'name': 'Ascension', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AU', 'name': 'Australia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AT', 'name': 'Austria', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'AZ', 'name': 'Azerbaijan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BH', 'name': 'Bahrain', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-81', 'name': 'Baker Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BD', 'name': 'Bangladesh', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BB', 'name': 'Barbados', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BY', 'name': 'Belarus', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BE', 'name': 'Belgium', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'BZ', 'name': 'Belize', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BJ', 'name': 'Benin', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BM', 'name': 'Bermuda', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BT', 'name': 'Bhutan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BO', 'name': 'Bolivia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BQ-BO', 'name': 'Bonaire', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BA', 'name': 'Bosnia and Herzegovina', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BW', 'name': 'Botswana', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BV', 'name': 'Bouvet Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BR', 'name': 'Brazil', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BAT', 'name': 'British Antarctic Territory', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'IO', 'name': 'British Indian Ocean Territory', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'VG', 'name': 'British Virgin Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BN', 'name': 'Brunei', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BG', 'name': 'Bulgaria', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'BF', 'name': 'Burkina Faso', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MM', 'name': 'Burma', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BI', 'name': 'Burundi', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KH', 'name': 'Cambodia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CM', 'name': 'Cameroon', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CA', 'name': 'Canada', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CV', 'name': 'Cape Verde', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KY', 'name': 'Cayman Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'CF', 'name': 'Central African Republic', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ES-CE', 'name': 'Ceuta', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TD', 'name': 'Chad', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CL', 'name': 'Chile', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CN', 'name': 'China', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CX', 'name': 'Christmas Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'CC', 'name': 'Cocos (Keeling) Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'CO', 'name': 'Colombia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KM', 'name': 'Comoros', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CG', 'name': 'Congo', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CD', 'name': 'Congo (Democratic Republic)', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CK', 'name': 'Cook Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'CR', 'name': 'Costa Rica', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'HR', 'name': 'Croatia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'CU', 'name': 'Cuba', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'CW', 'name': 'Curaçao', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'CY', 'name': 'Cyprus', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'CZ', 'name': 'Czechia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'DK', 'name': 'Denmark', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'XXD', 'name': 'Dhekelia', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'DJ', 'name': 'Djibouti', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'DM', 'name': 'Dominica', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'DO', 'name': 'Dominican Republic', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AE-DU', 'name': 'Dubai', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TL', 'name': 'East Timor', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'EC', 'name': 'Ecuador', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'EG', 'name': 'Egypt', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SV', 'name': 'El Salvador', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GQ', 'name': 'Equatorial Guinea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ER', 'name': 'Eritrea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'EE', 'name': 'Estonia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'SZ', 'name': 'Eswatini', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ET', 'name': 'Ethiopia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'FK', 'name': 'Falkland Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'FO', 'name': 'Faroe Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'FJ', 'name': 'Fiji', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'FI', 'name': 'Finland', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'FR', 'name': 'France', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'GF', 'name': 'French Guiana', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'PF', 'name': 'French Polynesia', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TF', 'name': 'French Southern Territories', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AE-FU', 'name': 'Fujairah', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GA', 'name': 'Gabon', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GE', 'name': 'Georgia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'DE', 'name': 'Germany', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'GH', 'name': 'Ghana', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GI', 'name': 'Gibraltar', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GR', 'name': 'Greece', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'GL', 'name': 'Greenland', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GD', 'name': 'Grenada', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GP', 'name': 'Guadeloupe', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GU', 'name': 'Guam', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GT', 'name': 'Guatemala', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GG', 'name': 'Guernsey', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'GN', 'name': 'Guinea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GW', 'name': 'Guinea-Bissau', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GY', 'name': 'Guyana', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'HT', 'name': 'Haiti', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'HM', 'name': 'Heard Island and McDonald Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'HN', 'name': 'Honduras', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'HK', 'name': 'Hong Kong', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'UM-84', 'name': 'Howland Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'HU', 'name': 'Hungary', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'IS', 'name': 'Iceland', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'IN', 'name': 'India', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ID', 'name': 'Indonesia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'IR', 'name': 'Iran', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'IQ', 'name': 'Iraq', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'IE', 'name': 'Ireland', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'IM', 'name': 'Isle of Man', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'IL', 'name': 'Israel', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'IT', 'name': 'Italy', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'CI', 'name': 'Ivory Coast', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'JM', 'name': 'Jamaica', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'JP', 'name': 'Japan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-86', 'name': 'Jarvis Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'JE', 'name': 'Jersey', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'UM-67', 'name': 'Johnston Atoll', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'JO', 'name': 'Jordan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KZ', 'name': 'Kazakhstan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KE', 'name': 'Kenya', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-89', 'name': 'Kingman Reef', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'KI', 'name': 'Kiribati', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'XK', 'name': 'Kosovo', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KW', 'name': 'Kuwait', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KG', 'name': 'Kyrgyzstan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LA', 'name': 'Laos', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LV', 'name': 'Latvia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'LB', 'name': 'Lebanon', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LS', 'name': 'Lesotho', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LR', 'name': 'Liberia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LY', 'name': 'Libya', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LI', 'name': 'Liechtenstein', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LT', 'name': 'Lithuania', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'LU', 'name': 'Luxembourg', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'MO', 'name': 'Macao', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MG', 'name': 'Madagascar', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MW', 'name': 'Malawi', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MY', 'name': 'Malaysia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MV', 'name': 'Maldives', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ML', 'name': 'Mali', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MT', 'name': 'Malta', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'MH', 'name': 'Marshall Islands', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MQ', 'name': 'Martinique', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MR', 'name': 'Mauritania', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MU', 'name': 'Mauritius', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'YT', 'name': 'Mayotte', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'ES-ML', 'name': 'Melilla', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MX', 'name': 'Mexico', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'FM', 'name': 'Micronesia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-71', 'name': 'Midway Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MD', 'name': 'Moldova', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MC', 'name': 'Monaco', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MN', 'name': 'Mongolia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ME', 'name': 'Montenegro', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MS', 'name': 'Montserrat', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MA', 'name': 'Morocco', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MZ', 'name': 'Mozambique', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NA', 'name': 'Namibia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NR', 'name': 'Nauru', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-76', 'name': 'Navassa Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'NP', 'name': 'Nepal', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NL', 'name': 'Netherlands', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'NC', 'name': 'New Caledonia', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'NZ', 'name': 'New Zealand', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NI', 'name': 'Nicaragua', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NE', 'name': 'Niger', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NG', 'name': 'Nigeria', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'NU', 'name': 'Niue', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'NF', 'name': 'Norfolk Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'KP', 'name': 'North Korea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MK', 'name': 'North Macedonia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'MP', 'name': 'Northern Mariana Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'NO', 'name': 'Norway', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PS', 'name': 'Occupied Palestinian Territories', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'OM', 'name': 'Oman', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PK', 'name': 'Pakistan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PW', 'name': 'Palau', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-95', 'name': 'Palmyra Atoll', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'PA', 'name': 'Panama', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PG', 'name': 'Papua New Guinea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PY', 'name': 'Paraguay', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PE', 'name': 'Peru', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PH', 'name': 'Philippines', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'PN', 'name': 'Pitcairn, Henderson, Ducie and Oeno Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'PL', 'name': 'Poland', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'PT', 'name': 'Portugal', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'PR', 'name': 'Puerto Rico', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'QA', 'name': 'Qatar', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AE-RK', 'name': 'Ras al-Khaimah', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'RE', 'name': 'Réunion', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'RO', 'name': 'Romania', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'RU', 'name': 'Russia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'RW', 'name': 'Rwanda', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BQ-SA', 'name': 'Saba', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'BL', 'name': 'Saint Barthélemy', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SH-HL', 'name': 'Saint Helena', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'PM', 'name': 'Saint Pierre and Miquelon', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'MF', 'name': 'Saint-Martin (French part)', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'WS', 'name': 'Samoa', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SM', 'name': 'San Marino', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ST', 'name': 'Sao Tome and Principe', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SA', 'name': 'Saudi Arabia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SN', 'name': 'Senegal', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'RS', 'name': 'Serbia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SC', 'name': 'Seychelles', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AE-SH', 'name': 'Sharjah', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SL', 'name': 'Sierra Leone', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SG', 'name': 'Singapore', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BQ-SE', 'name': 'Sint Eustatius', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SX', 'name': 'Sint Maarten (Dutch part)', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SK', 'name': 'Slovakia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'SI', 'name': 'Slovenia', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'SB', 'name': 'Solomon Islands', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SO', 'name': 'Somalia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ZA', 'name': 'South Africa', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GS', 'name': 'South Georgia and South Sandwich Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'KR', 'name': 'South Korea', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SS', 'name': 'South Sudan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ES', 'name': 'Spain', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'LK', 'name': 'Sri Lanka', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'KN', 'name': 'St Kitts and Nevis', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'LC', 'name': 'St Lucia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VC', 'name': 'St Vincent', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SD', 'name': 'Sudan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SR', 'name': 'Suriname', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SJ', 'name': 'Svalbard and Jan Mayen', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'SE', 'name': 'Sweden', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'CH', 'name': 'Switzerland', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SY', 'name': 'Syria', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TW', 'name': 'Taiwan', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TJ', 'name': 'Tajikistan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TZ', 'name': 'Tanzania', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TH', 'name': 'Thailand', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'BS', 'name': 'The Bahamas', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GM', 'name': 'The Gambia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TG', 'name': 'Togo', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TK', 'name': 'Tokelau', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TO', 'name': 'Tonga', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TT', 'name': 'Trinidad and Tobago', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'SH-TA', 'name': 'Tristan da Cunha', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TN', 'name': 'Tunisia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TR', 'name': 'Turkey', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TM', 'name': 'Turkmenistan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'TC', 'name': 'Turks and Caicos Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'TV', 'name': 'Tuvalu', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UG', 'name': 'Uganda', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UA', 'name': 'Ukraine', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'AE-UQ', 'name': 'Umm al-Quwain', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'AE', 'name': 'United Arab Emirates', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'GB', 'name': 'United Kingdom', 'type': 'gov.uk Country', 'is_eu': True},
        {'id': 'US', 'name': 'United States', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VI', 'name': 'United States Virgin Islands', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'UY', 'name': 'Uruguay', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UZ', 'name': 'Uzbekistan', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VU', 'name': 'Vanuatu', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VA', 'name': 'Vatican City', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VE', 'name': 'Venezuela', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'VN', 'name': 'Vietnam', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'UM-79', 'name': 'Wake Island', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'WF', 'name': 'Wallis and Futuna', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'EH', 'name': 'Western Sahara', 'type': 'gov.uk Territory', 'is_eu': False},
        {'id': 'YE', 'name': 'Yemen', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ZM', 'name': 'Zambia', 'type': 'gov.uk Country', 'is_eu': False},
        {'id': 'ZW', 'name': 'Zimbabwe', 'type': 'gov.uk Country', 'is_eu': False}]
    }


@pytest.fixture
def data_cases_search(data_case, data_second_case, mock_case_statuses, data_case_types):
    return {
        "count": 2,
        "results": {
            "cases": [data_case["case"], data_second_case["case"]],
            "filters": {
                "advice_types": [
                    {"key": "approve", "value": "Approve"},
                    {"key": "proviso", "value": "Proviso"},
                    {"key": "refuse", "value": "Refuse"},
                    {"key": "no_licence_required", "value": "No Licence Required"},
                    {"key": "not_applicable", "value": "Not Applicable"},
                    {"key": "conflicting", "value": "Conflicting"},
                ],
                "case_types": data_case_types,
                "gov_users": [{"full_name": "John Smith", "id": gov_uk_user_id}],
                "statuses": mock_case_statuses["statuses"],
                "is_system_queue": True,
                "is_work_queue": False,
                "queue": {"case_count": 2, "id": "00000000-0000-0000-0000-000000000001", "name": "All cases"},
            },
            "queues": [
                {"case_count": 2, "id": "00000000-0000-0000-0000-000000000001", "name": "All cases"},
                {"case_count": 2, "id": "00000000-0000-0000-0000-000000000002", "name": "Open cases"},
                {"case_count": 1, "id": "00000000-0000-0000-0000-000000000003", "name": "My team's cases"},
                {"case_count": 0, "id": "00000000-0000-0000-0000-000000000004", "name": "New exporter amendments"},
                {"case_count": 1, "id": "00000000-0000-0000-0000-000000000005", "name": "My assigned cases"},
                {"case_count": 1, "id": "00000000-0000-0000-0000-000000000006", "name": "My caseload"},
            ],
        },
        "total_pages": 1,
    }


@pytest.fixture
def case_pk(data_case):
    return data_case["case"]["id"]


@pytest.fixture
def mock_case(
    requests_mock,
    mock_case_ecju_queries,
    mock_case_assigned_queues,
    mock_case_documents,
    mock_case_additional_documents,
    mock_case_activity_filters,
    data_case,
):
    url = client._build_absolute_uri(f"/cases/{application_id}/")
    yield requests_mock.get(url=url, json=data_case)


@pytest.fixture
def data_queue():
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "All cases",
        "is_system_queue": True,
        "countersigning_queue": None,
    }


@pytest.fixture
def queue_pk(data_queue):
    return data_queue["id"]


@pytest.fixture
def mock_queue(requests_mock, data_queue):
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


@pytest.fixture
def mock_countries(requests_mock, data_countries):
    url = client._build_absolute_uri("/static/countries/" + convert_value_to_query_param("exclude", None))
    yield requests_mock.get(url=url, json=data_countries)


@pytest.fixture
def mock_cases_search(requests_mock, data_cases_search, queue_pk):
    encoded_params = parse.urlencode({"page": 1, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&{encoded_params}")
    yield requests_mock.get(url=url, json=data_cases_search)


@pytest.fixture(autouse=True)
def mock_status_properties(requests_mock):
    url = client._build_absolute_uri("/static/statuses/properties/")
    data = {"is_read_only": False, "is_terminal": False}
    requests_mock.get(url=re.compile(f"{url}.*/"), json=data)
    yield data


@pytest.fixture
def mock_gov_user(requests_mock, mock_notifications, mock_case_statuses):
    url = client._build_absolute_uri("/gov-users/")
    data = {
        "user": {
            "id": gov_uk_user_id,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
            "role": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Super User",
                "permissions": [
                    "ACTIVATE_FLAGS",
                    "ADMINISTER_ROLES",
                    "MANAGE_LICENCE_DURATION",
                    "REOPEN_CLOSED_CASES",
                    "MANAGE_TEAM_CONFIRM_OWN_ADVICE",
                    "CONFIGURE_TEMPLATES",
                    "MAINTAIN_FOOTNOTES",
                    "ENFORCEMENT_CHECK",
                    "MAINTAIN_OGL",
                    "MANAGE_ALL_ROUTING_RULES",
                    "MANAGE_CLEARANCE_FINAL_ADVICE",
                    "MANAGE_FLAGGING_RULES",
                    "MANAGE_LICENCE_FINAL_ADVICE",
                    "MANAGE_ORGANISATIONS",
                    "MANAGE_PICKLISTS",
                    "MANAGE_TEAM_ADVICE",
                    "MANAGE_TEAM_ROUTING_RULES",
                    "RESPOND_PV_GRADING",
                    "REVIEW_GOODS",
                ],
                "statuses": mock_case_statuses["statuses"],
            },
            "default_queue": {"id": "00000000-0000-0000-0000-000000000001", "name": "All cases"},
        }
    }

    requests_mock.get(url=f"{url}me/", json=data)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=data)

    yield data


@pytest.fixture
def mock_notifications(requests_mock):
    url = client._build_absolute_uri("/gov-users/notifications/")
    data = {"notifications": {"organisations": 8}, "has_notifications": True}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_ecju_queries(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/ecju-queries/")
    data = {"ecju_queries": []}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_assigned_queues(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/assigned-queues/")
    data = {"queues": []}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_documents(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/documents/")
    data = {
        "documents": [
            {
                "id": "c58f84b2-6925-4aee-9888-c3115e2fdc26",
                "name": "Application Form - 2020-08-03 12:52:37.977275+00:00.pdf",
                "type": {"key": "AUTO_GENERATED", "value": "Auto Generated"},
                "metadata_id": "c58f84b2-6925-4aee-9888-c3115e2fdc26",
                "user": None,
                "size": None,
                "case": application_id,
                "created_at": "2020-08-03T12:52:37.977338Z",
                "safe": True,
                "description": None,
                "visible_to_exporter": False,
            }
        ]
    }
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_additional_documents(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/additional-contacts/")
    data = []
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_activity_system_user(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/activity/")
    data = {
        "activity": [
            {
                "id": "1eaa6494-1fd3-4613-8a92-39b02d889fa9",
                "created_at": "2020-08-03T12:52:38.239382Z",
                "user": {"first_name": "LITE", "last_name": "system"},
                "text": "moved the case to queue 20200629162022.",
                "additional_text": "",
            },
            {
                "id": "ba08e46b-0278-40ff-87a2-8be2600fad49",
                "created_at": "2020-08-03T12:52:37.740574Z",
                "user": {"first_name": "Automated", "last_name": "Test"},
                "text": "updated the status to: Submitted.",
                "additional_text": "",
            },
        ]
    }
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_teams(requests_mock):
    url = client._build_absolute_uri("/teams/")
    data = {
        "teams": [
            {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
            {"id": "7d60e199-c64c-4863-bdd6-ac441f4fe806", "name": "Example team"},
        ]
    }
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_case_activity_filters(requests_mock):
    url = client._build_absolute_uri(f"/cases/{application_id}/activity/filters/")
    data = {
        "filters": {
            "activity_types": [
                {"key": "move_case", "value": "Move case"},
                {"key": "updated_status", "value": "Updated status"},
            ],
            "teams": [],
            "user_types": [{"key": "internal", "value": "Internal"}, {"key": "exporter", "value": "Exporter"}],
            "users": [
                {"key": "73402567-751c-41d7-9aa6-8061f1663db7", "value": "Automated Test"},
                {"key": "00000000-0000-0000-0000-000000000001", "value": "LITE system"},
            ],
        }
    }
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_blocking_flags(requests_mock):
    url = client._build_absolute_uri("/flags/")
    data = [
        {
            "id": "00000000-0000-0000-0000-000000000014",
            "name": "Enforcement Check Req",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_approval": True,
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        }
    ]
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_case_statuses(requests_mock):
    url = client._build_absolute_uri("/static/statuses/")
    data = {
        "statuses": [
            {"id": "00000000-0000-0000-0000-000000000001", "key": "submitted", "value": "Submitted", "priority": 1},
            {
                "id": "00000000-0000-0000-0000-000000000002",
                "key": "applicant_editing",
                "value": "Applicant editing",
                "priority": 2,
            },
            {"id": "00000000-0000-0000-0000-000000000003", "key": "resubmitted", "value": "Resubmitted", "priority": 3},
            {
                "id": "00000000-0000-0000-0000-000000000004",
                "key": "initial_checks",
                "value": "Initial checks",
                "priority": 4,
            },
            {
                "id": "00000000-0000-0000-0000-000000000005",
                "key": "under_review",
                "value": "Under review",
                "priority": 5,
            },
            {"id": "00000000-0000-0000-0000-000000000026", "key": "ogd_advice", "value": "OGD Advice", "priority": 6},
            {
                "id": "00000000-0000-0000-0000-000000000006",
                "key": "under_final_review",
                "value": "Under final review",
                "priority": 7,
            },
            {"id": "00000000-0000-0000-0000-000000000007", "key": "finalised", "value": "Finalised", "priority": 8},
            {"id": "00000000-0000-0000-0000-000000000023", "key": "clc_review", "value": "CLC review", "priority": 9},
            {
                "id": "00000000-0000-0000-0000-000000000024",
                "key": "pv_review",
                "value": "PV grading review",
                "priority": 10,
            },
            {"id": "00000000-0000-0000-0000-000000000027", "key": "open", "value": "Open", "priority": 11},
            {
                "id": "00000000-0000-0000-0000-000000000028",
                "key": "under_internal_review",
                "value": "Under internal review",
                "priority": 12,
            },
            {
                "id": "00000000-0000-0000-0000-000000000029",
                "key": "return_to_inspector",
                "value": "Return to inspector",
                "priority": 13,
            },
            {
                "id": "00000000-0000-0000-0000-000000000030",
                "key": "awaiting_exporter_response",
                "value": "Awaiting exporter response",
                "priority": 14,
            },
            {"id": "00000000-0000-0000-0000-000000000008", "key": "withdrawn", "value": "Withdrawn", "priority": 15},
            {"id": "00000000-0000-0000-0000-000000000009", "key": "closed", "value": "Closed", "priority": 16},
            {"id": "00000000-0000-0000-0000-000000000010", "key": "registered", "value": "Registered", "priority": 17},
            {
                "id": "00000000-0000-0000-0000-000000000011",
                "key": "under_appeal",
                "value": "Under appeal",
                "priority": 18,
            },
            {
                "id": "00000000-0000-0000-0000-000000000012",
                "key": "appeal_review",
                "value": "Appeal review",
                "priority": 19,
            },
            {
                "id": "00000000-0000-0000-0000-000000000013",
                "key": "appeal_final_review",
                "value": "Appeal final review",
                "priority": 20,
            },
            {
                "id": "00000000-0000-0000-0000-000000000014",
                "key": "reopened_for_changes",
                "value": "Re-opened for changes",
                "priority": 21,
            },
            {
                "id": "00000000-0000-0000-0000-000000000025",
                "key": "reopened_due_to_org_changes",
                "value": "Re-opened due to org changes",
                "priority": 22,
            },
            {
                "id": "00000000-0000-0000-0000-000000000015",
                "key": "change_initial_review",
                "value": "Change initial review",
                "priority": 23,
            },
            {
                "id": "00000000-0000-0000-0000-000000000016",
                "key": "change_under_review",
                "value": "Change under review",
                "priority": 24,
            },
            {
                "id": "00000000-0000-0000-0000-000000000017",
                "key": "change_under_final_review",
                "value": "Change under final review",
                "priority": 25,
            },
            {
                "id": "00000000-0000-0000-0000-000000000018",
                "key": "under_ECJU_review",
                "value": "Under ECJU appeal",
                "priority": 26,
            },
            {"id": "00000000-0000-0000-0000-000000000019", "key": "revoked", "value": "Revoked", "priority": 27},
            {"id": "00000000-0000-0000-0000-000000000020", "key": "suspended", "value": "Suspended", "priority": 28},
            {
                "id": "00000000-0000-0000-0000-000000000021",
                "key": "surrendered",
                "value": "Surrendered",
                "priority": 29,
            },
            {
                "id": "00000000-0000-0000-0000-000000000022",
                "key": "deregistered",
                "value": "De-registered",
                "priority": 30,
            },
        ]
    }
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def data_good_on_application(data_case):
    return {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
            "description": "444",
            "part_number": "44",
            "control_list_entries": [],
            "comment": None,
            "is_good_controlled": {"key": "False", "value": "No"},
            "report_summary": "",
            "flags": [],
            "documents": [],
            "is_pv_graded": "no",
            "grading_comment": None,
            "pv_grading_details": None,
            "status": {"key": "verified", "value": "Verified"},
            "item_category": {"key": "group1_device", "value": "Device, equipment or object"},
            "is_military_use": {"key": "no", "value": "No"},
            "is_component": {"key": "no", "value": "No"},
            "uses_information_security": False,
            "modified_military_use_details": None,
            "component_details": None,
            "information_security_details": None,
            "missing_document_reason": {"key": "OFFICIAL_SENSITIVE", "value": "Document is above OFFICIAL-SENSITIVE"},
            "software_or_technology_details": None,
            "firearm_details": None,
        },
        "application": data_case["case"]["id"],
        "quantity": 444.0,
        "unit": {"key": "GRM", "value": "Gram(s)"},
        "value": "444.00",
        "is_good_incorporated": False,
        "flags": [],
        "item_type": None,
        "other_item_type": None,
        "is_good_controlled": {"key": "True", "value": "Tes"},
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms..."},
            {"rating": "ML2", "text": "Smooth-bore weapons with a calibre of 20mm or more, other armament..."},
        ],
        "comment": "",
        "report_summary": "",
        "audit_trail": [
            {
                "id": "86f4d159-a282-4a25-b236-7e3d195356be",
                "created_at": "2020-10-07T15:26:36.976341+01:00",
                "user": {
                    "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                    "first_name": "Richard",
                    "last_name": "Tier",
                    "type": "internal",
                },
                "text": 'good was reviewed: 444 control code changed from "ML1" to "ML1, ML2".',
                "additional_text": "",
            },
            {
                "id": "fcd4f521-18b2-4efc-b011-aac841195a76",
                "created_at": "2020-10-07T15:22:09.786473+01:00",
                "user": {
                    "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                    "first_name": "Richard",
                    "last_name": "Tier",
                    "type": "internal",
                },
                "text": 'good was reviewed: 444 control code changed from "ML1, ML2" to "ML1".',
                "additional_text": "",
            },
        ],
    }


@pytest.fixture
def good_on_application_pk(data_good_on_application):
    return data_good_on_application["id"]


@pytest.fixture
def mock_good_on_appplication(requests_mock, mock_case, data_good_on_application):
    url = client._build_absolute_uri("/applications/good-on-application")
    yield requests_mock.get(url=re.compile(f"{url}.*"), json=data_good_on_application)


@pytest.fixture(autouse=True)
def data_search():
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "facets": {},
        "results": [
            {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                "queues": [{"id": "1b926457-5c9e-4916-8497-51886e51863a", "name": "queue", "team": "Admin"}],
                "name": "444",
                "reference_code": "GBSIEL/2020/0002687/T",
                "organisation": "jim",
                "status": "submitted",
                "case_type": "application",
                "case_subtype": "standard",
                "submitted_by": {"username": None, "email": "rikatee+wesd@gmail.com"},
                "created": "16:53 01 October 2020",
                "updated": "16:57 01 October 2020",
                "case_officer": {},
                "goods": [
                    {
                        "quantity": 444.0,
                        "value": 444.0,
                        "unit": "GRM",
                        "incorporated": False,
                        "description": "444",
                        "comment": None,
                        "part_number": "44",
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "control_list_entries": [],
                        "report_summary": "",
                    }
                ],
                "parties": [{"name": "44", "address": "44", "type": "end_user", "country": "United Kingdom"}],
                "highlight": {"goods.part_number.raw": ["<b>44</b>"]},
                "index": "lite",
                "score": 1.0,
            }
        ],
    }


@pytest.fixture(autouse=True)
def mock_search(requests_mock, data_search):
    url = client._build_absolute_uri("/search/application/application_search/")
    yield requests_mock.get(url=url, json=data_search)


@pytest.fixture
def authorized_client_factory(client: Client, settings):
    """
    returns a factory to make a authorized client for a mock_gov_user,

    the factory only expects the value of "user" inside the object returned by
    the mock_gov_user fixture
    """

    def _inner(user):
        session = client.session
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]
        session["default_queue"] = user["default_queue"]["id"]
        session["lite_api_user_id"] = user["id"]
        session[settings.TOKEN_SESSION_KEY] = {
            "access_token": "mock_access_token",
            "expires_in": 36000,
            "token_type": "Bearer",
            "scope": ["read", "write"],
            "refresh_token": "mock_refresh_token",
        }
        session.save()
        client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        return client

    yield _inner


@pytest.fixture
def authorized_client(mock_gov_user, authorized_client_factory):
    return authorized_client_factory(mock_gov_user["user"])
