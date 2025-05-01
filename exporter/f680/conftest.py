import pytest


@pytest.fixture
def data_f680_case(data_organisation):
    return {
        "id": "6cf7b401-62dc-4577-ad1d-4282f2aabc96",
        "application": {"name": "F680 Test 1"},
        "reference_code": None,
        "organisation": {
            "id": "3913ff20-5a2b-468a-bf5d-427228459b06",
            "name": "Archway Communications",
            "type": "commercial",
            "status": "active",
        },
        "submitted_at": None,
        "submitted_by": None,
        "name": "Test F680 Application",
        "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
        "case_type": {
            "id": "00000000-0000-0000-0000-000000000007",
            "reference": {"key": "f680", "value": "MOD F680 Clearance"},
            "sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"},
            "type": {"key": "security_clearance", "value": "Security Clearance"},
        },
    }


@pytest.fixture
def data_f680_submitted_application(data_f680_case):
    data_f680_case["reference_code"] = "F680/2025/0000001"
    data_f680_case["status"] = {"id": "00000000-0000-0000-0000-000000000001", "key": "submitted", "value": "Submitted"}
    data_f680_case["application"] = {
        "sections": {
            "general_application_details": {
                "type": "single",
                "label": "General application details",
                "fields": {
                    "name": {
                        "key": "name",
                        "answer": "F680 Test 1",
                        "datatype": "string",
                        "question": "Name the application",
                        "raw_answer": "F680 Test 1",
                    },
                    "is_exceptional_circumstances": {
                        "key": "is_exceptional_circumstances",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?",
                        "raw_answer": False,
                    },
                    "has_made_previous_application": {
                        "key": "has_made_previous_application",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Have you made a previous application?",
                        "raw_answer": False,
                    },
                },
                "fields_sequence": ["name", "has_made_previous_application", "is_exceptional_circumstances"],
            },
            "approval_type": {
                "type": "single",
                "label": "Approval type",
                "fields": {
                    "approval_choices": {
                        "key": "approval_choices",
                        "answer": ["Supply"],
                        "datatype": "list",
                        "question": "Select the types of approvals you need",
                        "raw_answer": ["supply"],
                    },
                    "demonstration_in_uk": {
                        "key": "demonstration_in_uk",
                        "answer": "",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "",
                    },
                    "approval_details_text": {
                        "key": "approval_details_text",
                        "answer": "cvxb",
                        "datatype": "string",
                        "question": "Provide details about what you're seeking approval to do",
                        "raw_answer": "cvxb",
                    },
                    "demonstration_overseas": {
                        "key": "demonstration_overseas",
                        "answer": "",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "",
                    },
                },
                "fields_sequence": [
                    "approval_choices",
                    "demonstration_in_uk",
                    "demonstration_overseas",
                    "approval_details_text",
                ],
            },
            "product_information": {
                "type": "single",
                "label": "Product information",
                "fields": {
                    "product_name": {
                        "key": "product_name",
                        "answer": "cb",
                        "datatype": "string",
                        "question": "Give the item a descriptive name",
                        "raw_answer": "cb",
                    },
                    "funding_source": {
                        "key": "funding_source",
                        "answer": "Private venture",
                        "datatype": "string",
                        "question": "Who is funding the item?",
                        "raw_answer": "private_venture",
                    },
                    "is_item_manpad": {
                        "key": "is_item_manpad",
                        "answer": "Don't know",
                        "datatype": "string",
                        "question": "Do you believe the item is a man-portable air defence system (MANPADS)?",
                        "raw_answer": "dont_know",
                    },
                    "actions_to_classify": {
                        "key": "actions_to_classify",
                        "answer": "cvb",
                        "datatype": "string",
                        "question": "Provide details on what action will have to be taken to have the product security classified",
                        "raw_answer": "cvb",
                    },
                    "product_description": {
                        "key": "product_description",
                        "answer": "cbv",
                        "datatype": "string",
                        "question": "Describe the item",
                        "raw_answer": "cbv",
                    },
                    "is_item_rated_under_mctr": {
                        "key": "is_item_rated_under_mctr",
                        "answer": "No, but the item supports a MTCR Category 1 item",
                        "datatype": "string",
                        "question": "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
                        "raw_answer": "supports_mtcr_1",
                    },
                    "is_used_by_uk_armed_forces": {
                        "key": "is_used_by_uk_armed_forces",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Will the item be used by the UK Armed Forces?",
                        "raw_answer": False,
                    },
                    "has_security_classification": {
                        "key": "has_security_classification",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Has the product been given a security classification by a UK MOD authority?",
                        "raw_answer": False,
                    },
                    "used_by_uk_armed_forces_info": {
                        "key": "used_by_uk_armed_forces_info",
                        "answer": "",
                        "datatype": "string",
                        "question": "Explain how it will be used",
                        "raw_answer": "",
                    },
                    "is_mod_electronic_data_shared": {
                        "key": "is_mod_electronic_data_shared",
                        "answer": "No",
                        "datatype": "string",
                        "question": "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?",
                        "raw_answer": "no",
                    },
                    "cryptography_or_security_feature_info": {
                        "key": "cryptography_or_security_feature_info",
                        "answer": "",
                        "datatype": "string",
                        "question": "Provide full details",
                        "raw_answer": "",
                    },
                    "is_foreign_tech_or_information_shared": {
                        "key": "is_foreign_tech_or_information_shared",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Will any foreign technology or information be shared with the item?",
                        "raw_answer": False,
                    },
                    "is_including_cryptography_or_security_features": {
                        "key": "is_including_cryptography_or_security_features",
                        "answer": "No",
                        "datatype": "boolean",
                        "question": "Does the item include cryptography or other information security features?",
                        "raw_answer": False,
                    },
                },
                "fields_sequence": [
                    "product_name",
                    "product_description",
                    "has_security_classification",
                    "actions_to_classify",
                    "is_foreign_tech_or_information_shared",
                    "is_including_cryptography_or_security_features",
                    "cryptography_or_security_feature_info",
                    "is_item_rated_under_mctr",
                    "is_item_manpad",
                    "is_mod_electronic_data_shared",
                    "funding_source",
                    "is_used_by_uk_armed_forces",
                    "used_by_uk_armed_forces_info",
                ],
            },
            "user_information": None,
            "supporting_documents": None,
            "notes_for_case_officers": None,
        }
    }
    return data_f680_case
