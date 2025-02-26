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
                "fields": [
                    {
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
                    {
                        "key": "demonstration_in_uk",
                        "answer": "some UK demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some UK demonstration reason",
                    },
                    {
                        "key": "demonstration_overseas",
                        "answer": "some overseas demonstration reason",
                        "datatype": "string",
                        "question": "Explain what you are demonstrating and why",
                        "raw_answer": "some overseas demonstration reason",
                    },
                    {
                        "key": "approval_details_text",
                        "answer": "some details",
                        "datatype": "string",
                        "question": "Provide details about what you're seeking approval to do",
                        "raw_answer": "some details",
                    },
                ],
            },
            "product_information": {
                "label": "Product information",
                "fields": [
                    {
                        "key": "product_name",
                        "answer": "Test Info",
                        "raw_answer": "Test Info",
                        "question": "Give the item a descriptive name",
                        "datatype": "string",
                    },
                    {
                        "key": "product_description",
                        "answer": "It does things",
                        "raw_answer": "It does things",
                        "question": "Describe the item",
                        "datatype": "string",
                    },
                    {
                        "key": "is_foreign_tech_or_information_shared",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Will any foreign technology or information be shared with the item?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "is_controlled_under_itar",
                        "answer": "Yes, it's controlled under  ITAR",
                        "raw_answer": True,
                        "question": "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "controlled_info",
                        "answer": "It just is",
                        "raw_answer": "It just is",
                        "question": "Explain how the technology or information is controlled. Include countries classification levels and reference"
                        "numbers. You can upload supporting documents later in your application",
                        "datatype": "string",
                    },
                    {
                        "key": "controlled_information",
                        "answer": "Some info",
                        "raw_answer": "Some info",
                        "question": "What is the ITAR controlled technology or information?",
                        "datatype": "string",
                    },
                    {
                        "key": "itar_reference_number",
                        "answer": "123456",
                        "raw_answer": "123456",
                        "question": "ITAR reference number",
                        "datatype": "string",
                    },
                    {
                        "key": "usml_categories",
                        "answer": "cat 1",
                        "raw_answer": "cat 1",
                        "question": "What are the United States Munitions List (USML) categories listed on your ITAR approval?",
                        "datatype": "string",
                    },
                    {
                        "key": "itar_approval_scope",
                        "answer": "no scope",
                        "raw_answer": "no scope",
                        "question": "Describe the scope of your ITAR approval",
                        "datatype": "string",
                    },
                    {
                        "key": "expected_time_in_possession",
                        "answer": "10 years",
                        "raw_answer": "10 years",
                        "question": "How long do you expect the technology or information that is controlled under the US ITAR to be in your possession?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_including_cryptography_or_security_features",
                        "answer": "Yes",
                        "raw_answer": True,
                        "question": "Does the item include cryptography or other information security features?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "cryptography_or_security_feature_info",
                        "answer": "some",
                        "raw_answer": "some",
                        "question": "Provide full details",
                        "datatype": "string",
                    },
                    {
                        "key": "is_item_rated_under_mctr",
                        "answer": "Yes, the product is MTCR Category 1",
                        "raw_answer": "mtcr_1",
                        "question": "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
                        "datatype": "string",
                    },
                    {
                        "key": "is_item_manpad",
                        "answer": "No, the product is not a MANPAD",
                        "raw_answer": "no",
                        "question": "Do you believe the item is a man-portable air defence system (MANPAD)?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_mod_electronic_data_shared",
                        "answer": "No",
                        "raw_answer": "no",
                        "question": "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?",
                        "datatype": "string",
                    },
                    {
                        "key": "funding_source",
                        "answer": "MOD",
                        "raw_answer": "mod",
                        "question": "Who is funding the item?",
                        "datatype": "string",
                    },
                    {
                        "key": "is_used_by_uk_armed_forces",
                        "answer": "No",
                        "raw_answer": False,
                        "question": "Will the item be used by the UK Armed Forces?",
                        "datatype": "boolean",
                    },
                    {
                        "key": "used_by_uk_armed_forces_info",
                        "answer": "",
                        "raw_answer": "",
                        "question": "Explain how it will be used",
                        "datatype": "string",
                    },
                ],
                "type": "single",
            },
        }
    }
    application_id = data_f680_case["id"]
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)
