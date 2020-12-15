import pytest

from core import client


@pytest.fixture
def data_control_list_entries():
    # in relity there are around 3000 CLCs
    return {
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms..."},
            {"rating": "ML1a", "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns"},
        ]
    }


@pytest.fixture
def mock_control_list_entries(requests_mock, data_control_list_entries):
    url = client._build_absolute_uri("/static/control-list-entries/")
    yield requests_mock.get(url=url, json=data_control_list_entries)


@pytest.fixture
def mock_pv_gradings(requests_mock):
    url = client._build_absolute_uri("/static/private-venture-gradings/")
    yield requests_mock.get(url=url, json={"pv_gradings": []})


@pytest.fixture
def data_open_case():
    return {
        "case": {
            "id": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
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
                "id": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
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
                "case": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
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
                        "control_list_entries": [{"rating": "ML1a", "text": "Outmoded bourgeois reactionaries",}],
                        "countries": [{"id": "US", "name": "United States", "type": "gov.uk Country", "is_eu": False}],
                        "document": None,
                        "end_use_control": ["MEND"],
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
                        "application": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
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
def data_standard_case():
    return {
        "case": {
            "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000004",
                "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                "type": {"key": "application", "value": "Application"},
                "sub_type": {"key": "standard", "value": "Standard Licence"},
            },
            "flags": [
                {
                    "id": "00000000-0000-0000-0000-000000000014",
                    "name": "Enforcement Check Req",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                }
            ],
            "queues": ["1b926457-5c9e-4916-8497-51886e51863a", "c270b79b-370c-4c5e-b8b6-4d5210a58956"],
            "queue_names": ["queue", "queue 20200818000000"],
            "assigned_users": {},
            "has_advice": {"user": False, "my_user": False, "team": False, "my_team": False, "final": False,},
            "advice": [],
            "all_flags": [
                {"name": "Enforcement Check Req", "label": None, "colour": "default", "priority": 0, "level": "Case",}
            ],
            "case_officer": None,
            "audit_notification": None,
            "reference_code": "GBSIEL/2020/0002687/T",
            "copy_of": None,
            "sla_days": 2,
            "sla_remaining_days": 18,
            "data": {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                "name": "444",
                "organisation": {
                    "id": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "primary_site": {
                        "id": "c86d3df2-5f48-40cd-a720-e76322df71a9",
                        "name": "Rich org",
                        "address": {
                            "id": "8d8a7631-32fc-4873-9a1f-d5e9afeecc0e",
                            "address_line_1": "jim",
                            "address_line_2": "",
                            "city": "jim",
                            "region": "Richardaho",
                            "postcode": "Dn22 6uh",
                            "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True,},
                        },
                        "records_located_at": {
                            "id": "c86d3df2-5f48-40cd-a720-e76322df71a9",
                            "name": "Rich org",
                            "address": {
                                "address_line_1": "jim",
                                "address_line_2": "",
                                "region": "Richardaho",
                                "postcode": "Dn22 6uh",
                                "city": "jim",
                                "country": {"name": "United Kingdom"},
                            },
                        },
                    },
                    "type": {"key": "commercial", "value": "Commercial Organisation"},
                    "flags": [],
                    "status": {"key": "active", "value": "Active"},
                    "created_at": "2020-09-15T10:04:02.741198+01:00",
                    "updated_at": "2020-09-15T10:04:27.663252+01:00",
                    "name": "jim",
                    "eori_number": "GB123456789000",
                    "sic_number": "99715",
                    "vat_number": "GB980941362",
                    "registration_number": "37718958",
                },
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000004",
                    "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "standard", "value": "Standard Licence"},
                },
                "export_type": {"key": "temporary", "value": "Temporary"},
                "created_at": "2020-10-01T16:53:58.578579+01:00",
                "updated_at": "2020-10-01T16:57:11.127857+01:00",
                "submitted_at": "2020-10-01T16:57:11.125297+01:00",
                "submitted_by": "rich tier",
                "status": {"key": "submitted", "value": "Submitted"},
                "case": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                "reference_code": "GBSIEL/2020/0002687/T",
                "is_major_editable": False,
                "goods_locations": {
                    "type": "external_locations",
                    "data": [
                        {
                            "id": "149edce6-529e-41c1-a4b3-48df06bfe5a1",
                            "name": "44",
                            "address": "44",
                            "country": {"id": "BN", "name": "Brunei", "type": "gov.uk Country", "is_eu": False},
                            "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                        }
                    ],
                },
                "case_officer": None,
                "end_user": {
                    "id": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "name": "44",
                    "address": "44",
                    "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True,},
                    "website": "",
                    "type": "end_user",
                    "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "document": None,
                    "sub_type": {"key": "individual", "value": "Individual"},
                    "sub_type_other": None,
                    "role": {"key": "other", "value": "Other"},
                    "role_other": None,
                    "flags": [],
                    "copy_of": None,
                    "deleted_at": None,
                    "clearance_level": None,
                    "descriptors": None,
                },
                "ultimate_end_users": [],
                "third_parties": [
                    {
                        "id": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                        "name": "44",
                        "address": "44",
                        "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        "website": "",
                        "type": "third_party",
                        "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                        "document": None,
                        "sub_type": {"key": "individual", "value": "Individual"},
                        "sub_type_other": None,
                        "role": {"key": "consultant", "value": "Consultant"},
                        "role_other": None,
                        "flags": [],
                        "copy_of": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                        "deleted_at": None,
                        "clearance_level": None,
                        "descriptors": None,
                    }
                ],
                "consignee": {
                    "id": "cd2263b4-a427-4f14-8552-505e1d192bb8",
                    "name": "44",
                    "address": "44",
                    "country": {"id": "AE-AZ", "name": "Abu Dhabi", "type": "gov.uk Territory", "is_eu": False,},
                    "website": "",
                    "type": "consignee",
                    "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "document": None,
                    "sub_type": {"key": "individual", "value": "Individual"},
                    "sub_type_other": None,
                    "role": {"key": "other", "value": "Other"},
                    "role_other": None,
                    "flags": [],
                    "copy_of": None,
                    "deleted_at": None,
                    "clearance_level": None,
                    "descriptors": None,
                },
                "inactive_parties": [],
                "goods": [
                    {
                        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                        "good": {
                            "id": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                            "description": "444",
                            "part_number": "44",
                            "control_list_entries": [],
                            "comment": None,
                            "is_good_controlled": {"key": "False", "value": "No"},
                            "report_summary": "scale compelling technologies",
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
                            "missing_document_reason": {
                                "key": "OFFICIAL_SENSITIVE",
                                "value": "Document is above OFFICIAL-SENSITIVE",
                            },
                            "software_or_technology_details": None,
                            "firearm_details": None,
                        },
                        "application": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                        "quantity": 444.0,
                        "unit": {"key": "GRM", "value": "Gram(s)"},
                        "value": "444.00",
                        "is_good_incorporated": False,
                        "flags": [],
                        "item_type": None,
                        "other_item_type": None,
                        "end_use_control": ["MEND"],
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "control_list_entries": [
                            {"rating": "ML8a", "text": '"Explosives" and mixtures of explosive substances'},
                            {"rating": "ML9a", "text": 'Naval "vessels" and components'},
                        ],
                        "comment": "hmmmhhh",
                        "report_summary": "scale compelling technologies",
                        "audit_trail": [],
                    }
                ],
                "have_you_been_informed": "no",
                "reference_number_on_information_form": None,
                "activity": "Brokering",
                "usage": None,
                "destinations": {
                    "type": "end_user",
                    "data": [
                        {
                            "id": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                            "name": "44",
                            "address": "44",
                            "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True,},
                            "website": "",
                            "type": "end_user",
                            "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                            "document": None,
                            "sub_type": {"key": "individual", "value": "Individual"},
                            "sub_type_other": None,
                            "role": {"key": "other", "value": "Other"},
                            "role_other": None,
                            "flags": [],
                            "copy_of": None,
                            "deleted_at": None,
                            "clearance_level": None,
                            "descriptors": None,
                        },
                    ],
                },
                "additional_documents": [],
                "is_military_end_use_controls": False,
                "military_end_use_controls_ref": None,
                "is_informed_wmd": False,
                "informed_wmd_ref": None,
                "is_suspected_wmd": False,
                "suspected_wmd_ref": None,
                "is_eu_military": False,
                "is_compliant_limitations_eu": None,
                "compliant_limitations_eu_ref": None,
                "intended_end_use": "44",
                "licence": None,
                "is_shipped_waybill_or_lading": False,
                "non_waybill_or_lading_route_details": "44",
                "temp_export_details": "44",
                "is_temp_direct_control": False,
                "temp_direct_control_details": "44",
                "proposed_return_date": "2021-01-01",
                "trade_control_activity": {"key": None, "value": None},
                "trade_control_product_categories": [],
            },
            "next_review_date": None,
            "licences": [],
        }
    }


@pytest.fixture
def data_good_on_application(data_standard_case):
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
        "application": data_standard_case["case"]["id"],
        "quantity": 444.0,
        "unit": {"key": "GRM", "value": "Gram(s)"},
        "value": "444.00",
        "is_good_incorporated": False,
        "flags": [],
        "item_type": None,
        "other_item_type": None,
        "is_good_controlled": {"key": "True", "value": "Yes"},
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons..."},
            {"rating": "ML2", "text": "Smooth-bore weapons..."},
        ],
        "end_use_control": ["MEND"],
        "comment": "",
        "report_summary": "",
        "good_on_application_documents": [],
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
