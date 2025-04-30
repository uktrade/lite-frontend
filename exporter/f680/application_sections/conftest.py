import pytest

from core import client


@pytest.fixture()
def unset_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def missing_application_id():
    return "6bb0828c-1520-4624-b729-7f3e6e5b9f5d"


@pytest.fixture
def mock_f680_application_get_404(requests_mock, missing_application_id):
    url = client._build_absolute_uri(f"/exporter/f680/application/{missing_application_id}/")
    return requests_mock.get(url=url, json={}, status_code=404)


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_patch_f680_application(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.patch(url=url, json=data_f680_case)


@pytest.fixture
def mock_patch_f680_application_no_user_information_items(requests_mock, data_f680_case):
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.patch(
        url=url,
        json={
            "name": "vfd",
            "sections": {"user_information": {"items": [], "label": "User Information", "type": "multiple"}},
        },
    )


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
    }


@pytest.fixture
def mock_f680_application_get_existing_data(requests_mock, data_f680_case):
    data_f680_case["application"] = {
        "sections": {
            "approval_type": {
                "type": "single",
                "label": "Approval type",
                "fields": {
                    "approval_choices": {
                        "key": "approval_choices",
                        "answer": [
                            "Initial discussions or promoting products",
                            "Demonstration in the United Kingdom to overseas customers",
                            "Demonstration overseas",
                            "Training",
                            "Through life support",
                            "Supply",
                        ],
                        "datatype": "list",
                        "question": "Select the types of approvals you need",
                        "raw_answer": [
                            "initial_discussion_or_promoting",
                            "demonstration_in_uk",
                            "demonstration_overseas",
                            "training",
                            "through_life_support",
                            "supply",
                        ],
                    },
                    "demonstration_in_uk": {
                        "key": "demonstration_in_uk",
                        "answer": "some UK demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some UK demonstration reason",
                    },
                    "demonstration_overseas": {
                        "key": "demonstration_overseas",
                        "answer": "some overseas demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some overseas demonstration reason",
                    },
                    "approval_details_text": {
                        "key": "approval_details_text",
                        "answer": "some details",
                        "datatype": "string",
                        "question": "Provide details about what you're seeking approval to do",
                        "raw_answer": "some details",
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
                "label": "Product information",
                "fields": {
                    "product_name": {
                        "key": "product_name",
                        "answer": "Test Info",
                        "raw_answer": "Test Info",
                        "question": "Give the item a descriptive name",
                        "datatype": "string",
                    },
                    "product_description": {
                        "key": "product_description",
                        "answer": "It does things",
                        "raw_answer": "It does things",
                        "question": "Describe the item",
                        "datatype": "string",
                    },
                    "has_security_classification": {
                        "key": "has_security_classification",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "What is the maximum security classification given?",
                        "datatype": "boolean",
                    },
                    "prefix": {
                        "key": "prefix",
                        "answer": "some prefix",
                        "raw_answer": "some prefix",
                        "question": "Enter a prefix (optional)",
                        "datatype": "string",
                    },
                    "actions_to_classify": {
                        "key": "actions_to_classify",
                        "answer": "some actions",
                        "raw_answer": "some actions",
                        "question": "Provide details on what action will have to be taken to have the product security classified",
                        "datatype": "string",
                    },
                    "security_classification": {
                        "key": "security_classification",
                        "answer": "unclassified",
                        "raw_answer": "unclassified",
                        "question": "Select security classification",
                        "datatype": "string",
                    },
                    "suffix": {
                        "key": "suffix",
                        "answer": "some suffix",
                        "raw_answer": "some suffix",
                        "question": "Enter a suffix (optional)",
                        "datatype": "string",
                    },
                    "issuing_authority_name_address": {
                        "key": "issuing_authority_name_address",
                        "answer": "Some address",
                        "raw_answer": "Some address",
                        "question": "Name and address of the issuing authority",
                        "datatype": "string",
                    },
                    "reference": {
                        "key": "reference",
                        "answer": "1234",
                        "raw_answer": "1234",
                        "question": "Reference",
                        "datatype": "string",
                    },
                    "date_of_issue": {
                        "key": "date_of_issue",
                        "answer": "2024-01-01",
                        "raw_answer": "2024-01-01",
                        "question": "Date of issue",
                        "datatype": "date",
                    },
                    "is_foreign_tech_or_information_shared": {
                        "key": "is_foreign_tech_or_information_shared",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Will any foreign technology or information be shared with the item?",
                        "datatype": "boolean",
                    },
                    "is_controlled_under_itar": {
                        "key": "is_controlled_under_itar",
                        "answer": "Yes, it's controlled under  ITAR",
                        "raw_answer": True,
                        "question": "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?",
                        "datatype": "boolean",
                    },
                    "controlled_info": {
                        "key": "controlled_info",
                        "answer": "It just is",
                        "raw_answer": "It just is",
                        "question": (
                            "Explain how the technology or information is controlled."
                            "Include countries classification levels and reference numbers. You can upload supporting documents later in your application"
                        ),
                        "datatype": "string",
                    },
                    "controlled_information": {
                        "key": "controlled_information",
                        "answer": "Some info",
                        "raw_answer": "Some info",
                        "question": "What is the ITAR controlled technology or information?",
                        "datatype": "string",
                    },
                    "itar_reference_number": {
                        "key": "itar_reference_number",
                        "answer": "123456",
                        "raw_answer": "123456",
                        "question": "ITAR reference number",
                        "datatype": "string",
                    },
                    "usml_categories": {
                        "key": "usml_categories",
                        "answer": "cat 1",
                        "raw_answer": "cat 1",
                        "question": "What are the United States Munitions List (USML) categories listed on your ITAR approval?",
                        "datatype": "string",
                    },
                    "itar_approval_scope": {
                        "key": "itar_approval_scope",
                        "answer": "no scope",
                        "raw_answer": "no scope",
                        "question": "Describe the scope of your ITAR approval",
                        "datatype": "string",
                    },
                    "expected_time_in_possession": {
                        "key": "expected_time_in_possession",
                        "answer": "10 years",
                        "raw_answer": "10 years",
                        "question": "How long do you expect the technology or information that is controlled under the US ITAR to be in your possession?",
                        "datatype": "string",
                    },
                    "is_including_cryptography_or_security_features": {
                        "key": "is_including_cryptography_or_security_features",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Does the item include cryptography or other information security features?",
                        "datatype": "boolean",
                    },
                    "cryptography_or_security_feature_info": {
                        "key": "cryptography_or_security_feature_info",
                        "answer": "some",
                        "raw_answer": "some",
                        "question": "Provide full details",
                        "datatype": "string",
                    },
                    "is_item_rated_under_mctr": {
                        "key": "is_item_rated_under_mctr",
                        "answer": "Yes, the product is MTCR Category 1",
                        "raw_answer": "mtcr_1",
                        "question": "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
                        "datatype": "string",
                    },
                    "is_item_manpad": {
                        "key": "is_item_manpad",
                        "answer": "No, the product is not a MANPADS",
                        "raw_answer": "no",
                        "question": "Do you believe the item is a man-portable air defence system (MANPADS)?",
                        "datatype": "string",
                    },
                    "is_mod_electronic_data_shared": {
                        "key": "is_mod_electronic_data_shared",
                        "answer": "No",
                        "raw_answer": "no",
                        "question": "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?",
                        "datatype": "string",
                    },
                    "funding_source": {
                        "key": "funding_source",
                        "answer": "MOD",
                        "raw_answer": "mod",
                        "question": "Who is funding the item?",
                        "datatype": "string",
                    },
                    "is_used_by_uk_armed_forces": {
                        "key": "is_used_by_uk_armed_forces",
                        "answer": "No",
                        "raw_answer": False,
                        "question": "Will the item be used by the UK Armed Forces?",
                        "datatype": "boolean",
                    },
                    "used_by_uk_armed_forces_info": {
                        "key": "used_by_uk_armed_forces_info",
                        "answer": "",
                        "raw_answer": "",
                        "question": "Explain how it will be used",
                        "datatype": "string",
                    },
                },
                "type": "single",
                "fields_sequence": [
                    "product_name",
                    "product_description",
                    "has_security_classification",
                    "prefix",
                    "actions_to_classify",
                    "security_classification",
                    "suffix",
                    "issuing_authority_name_address",
                    "reference",
                    "date_of_issue",
                    "is_foreign_tech_or_information_shared",
                    "is_controlled_under_itar",
                    "controlled_info",
                    "controlled_information",
                    "itar_reference_number",
                    "usml_categories",
                    "itar_approval_scope",
                    "expected_time_in_possession",
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
        }
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)
