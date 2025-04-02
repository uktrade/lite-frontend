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
def application_id(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def mock_application_get(requests_mock, data_standard_case):
    application = data_standard_case["case"]["data"]
    url = client._build_absolute_uri(f'/applications/{application["id"]}/')
    return requests_mock.get(url=url, json=application)


@pytest.fixture
def application_history(data_standard_case):
    return {
        "id": data_standard_case["case"]["data"]["id"],
        "reference_code": data_standard_case["case"]["data"]["reference_code"],
        "amendment_history": [
            {
                "status": {"status": "submitted", "status_display": "Submitted"},
                "ecju_query_count": 0,
                "reference_code": data_standard_case["case"]["data"]["reference_code"],
                "submitted_at": data_standard_case["case"]["data"]["submitted_at"],
                "id": data_standard_case["case"]["data"]["id"],  # /PS-IGNORE
            },
            {
                "status": {"status": "superseded_by_exporter_edit", "status_display": "Superseded by exporter edit"},
                "ecju_query_count": 3,
                "reference_code": "GBSIEL/2025/0000333/T",
                "submitted_at": "2025-01-27T16:36:27.185326Z",
                "id": "caba228c-b4c8-41ea-804a-c1bc6ba816c7",  # /PS-IGNORE
            },
        ],
    }


@pytest.fixture
def mock_application_history_get(requests_mock, application_history):
    url = client._build_absolute_uri(f'/exporter/applications/{application_history["id"]}/history')
    return requests_mock.get(url=url, json=application_history)


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
def mock_application_status_post(requests_mock, application_id):
    url = client._build_absolute_uri(f"/exporter/applications/{application_id}/status/")
    return requests_mock.post(url=url, json={})


@pytest.fixture
def mock_application_status_post_failure(requests_mock, application_id):
    url = client._build_absolute_uri(f"/exporter/applications/{application_id}/status/")
    return requests_mock.post(url=url, json={"error": "unexpected error"}, status_code=500)


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
def data_goa_good_incorporated(data_standard_case):
    return {
        "id": str(uuid.uuid4()),
        "created_at": "2024-03-26T15:22:35.714893Z",
        "updated_at": "2024-03-26T15:22:35.714893Z",
        "good": {
            "id": str(uuid.uuid4()),
            "name": "medium shotgun component",
            "description": "",
            "part_number": "",
            "no_part_number_comments": "",
            "control_list_entries": [
                {
                    "id": "0b9116c2-3aa0-49fb-a590-944b4738b208",  # /PS-IGNORE
                    "rating": "ML1a",
                    "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns",
                }
            ],
            "is_good_controlled": {"key": "True", "value": "Yes"},
            "flags": [],
            "documents": [],
            "is_pv_graded": "no",
            "status": {"key": "draft", "value": "Draft"},
            "item_category": {"key": "group2_firearms", "value": "Firearm"},
            "is_document_available": False,
            "no_document_comments": "asdf",
            "firearm_details": {
                "type": {
                    "key": "components_for_firearms",
                    "value": "Components for firearms",
                },
                "year_of_manufacture": 0,
                "calibre": "1",
                "replica_description": "",
                "is_covered_by_firearm_act_section_one_two_or_five": "No",
                "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
                "firearms_act_section": "",
                "section_certificate_missing_reason": "",
                "serial_numbers_available": "LATER",
                "no_proof_mark_details": "",
                "deactivation_standard": "",
                "deactivation_standard_other": "",
                "number_of_items": 1,
                "serial_numbers": [],
                "not_deactivated_to_standard_comments": "",
            },
            "is_precedent": False,
            "product_description": "",
        },
        "application": data_standard_case["case"]["id"],
        "quantity": 1.0,
        "unit": {"key": "NAR", "value": "Items"},
        "value": "1.00",
        "is_good_incorporated": True,
        "flags": [],
        "control_list_entries": [],
        "end_use_control": [],
        "audit_trail": [],
        "firearm_details": {
            "type": {
                "key": "components_for_firearms",
                "value": "Components for firearms",
            },
            "year_of_manufacture": 0,
            "calibre": "1",
            "replica_description": "",
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "firearms_act_section": "",
            "section_certificate_missing_reason": "",
            "serial_numbers_available": "LATER",
            "no_proof_mark_details": "",
            "is_deactivated": False,
            "deactivation_standard": "",
            "deactivation_standard_other": "",
            "number_of_items": 1,
            "serial_numbers": [],
            "not_deactivated_to_standard_comments": "",
        },
        "is_precedent": False,
        "is_onward_altered_processed_comments": "",
        "is_onward_incorporated_comments": "",
        "regime_entries": [],
        "nsg_list_type": "",
        "nsg_assessment_note": "",
    }


@pytest.fixture
def data_goa_onward_incorporated(data_standard_case):
    return {
        "id": str(uuid.uuid4()),
        "created_at": "2024-03-25T10:54:01.465094Z",
        "updated_at": "2024-03-25T10:54:01.465094Z",
        "good": {
            "id": str(uuid.uuid4()),
            "name": "medium size widget",
            "description": "",
            "part_number": "asdf",
            "no_part_number_comments": "",
            "control_list_entries": [],
            "is_good_controlled": {"key": "False", "value": "No"},
            "flags": [],
            "documents": [],
            "is_pv_graded": "no",
            "status": {"key": "draft", "value": "Draft"},
            "item_category": {
                "key": "group1_components",
                "value": "Component, accessory or module",
            },
            "is_military_use": {"key": "no", "value": "No"},
            "is_component": {
                "key": "yes_general",
                "value": "Yes, it's a general purpose component",
            },
            "uses_information_security": False,
            "component_details": "asdf",
            "information_security_details": "",
            "is_document_available": False,
            "no_document_comments": "asdf",
            "is_precedent": False,
            "product_description": "asdf",
        },
        "application": data_standard_case["case"]["id"],
        "quantity": 1.0,
        "unit": {"key": "NAR", "value": "Items"},
        "value": "1.00",
        "is_good_incorporated": False,
        "flags": [],
        "control_list_entries": [],
        "end_use_control": [],
        "audit_trail": [],
        "is_precedent": False,
        "is_onward_exported": True,
        "is_onward_altered_processed": False,
        "is_onward_altered_processed_comments": "",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "asdf",
        "regime_entries": [],
        "nsg_list_type": "",
        "nsg_assessment_note": "",
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
def application_products_url(data_standard_case):
    return reverse(
        "applications:goods",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


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
    clc_url = client._build_absolute_uri("/exporter/static/control-list-entries/")
    matcher = requests_mock.get(url=clc_url, json=[{"rating": "ML1"}, {"rating": "ML1a"}])
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


@pytest.fixture
def application_edit_type_url(application_id):
    return reverse(f"applications:edit_type", kwargs={"pk": application_id})


@pytest.fixture
def application_task_list_url(application_id):
    return reverse("applications:task_list", kwargs={"pk": application_id})


@pytest.fixture
def application_major_edit_existing_confirm_url(application_id):
    return reverse(f"applications:edit_type", kwargs={"pk": application_id})


@pytest.fixture
def application_major_edit_confirm_url(application_id):
    return reverse(f"applications:major_edit_confirm", kwargs={"pk": application_id})


@pytest.fixture
def data_f680_case(data_organisation):
    return {
        "id": "6cf7b401-62dc-4577-ad1d-4282f2aabc96",
        "application": {"name": "F680 Test 1"},
        "reference_code": "F680/2025/0000001",
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
def data_f680_submitted_application(data_f680_case):
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
                        "question": "Do you believe the item is a man-portable air defence system (MANPAD)?",
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
                        "question": "Has the product been given a security classifcation by a UK MOD authority?",
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
            "user_information": None,
            "supporting_documents": None,
            "notes_for_case_officers": None,
        }
    }
    return data_f680_case
