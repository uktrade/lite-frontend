import pytest

from datetime import timedelta

from django.utils import timezone

from core import client


@pytest.fixture
def data_f680_case(f680_case_id, f680_reference_code):
    submitted_at = timezone.now() - timedelta(days=7)
    return {
        "case": {
            "advice": [],
            "all_flags": [],
            "amendment_of": None,
            "assigned_users": {},
            "case_officer": None,
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000007",
                "reference": {"key": "f680", "value": "MOD F680 Clearance"},
                "sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"},
                "type": {"key": "application", "value": "Application"},
            },
            "copy_of": None,
            "countersign_advice": [],
            "data": {
                "application": {
                    "sections": {
                        "general_application_details": {
                            "label": "General application details",
                            "type": "single",
                            "fields": [
                                {
                                    "key": "name",
                                    "answer": "some name",
                                    "datatype": "string",
                                    "question": "Name the application",
                                    "raw_answer": "casdc",
                                },
                                {
                                    "key": "is_exceptional_circumstances",
                                    "answer": "No",
                                    "datatype": "boolean",
                                    "question": "Do you have exceptional circumstances that mean you need F680 approval in less than 30 days?",
                                    "raw_answer": False,
                                },
                            ],
                        },
                    }
                },
                "id": f680_case_id,
                "organisation": {
                    "id": "1363b104-9669-4c53-8602-8fc3717b07cd",  # /PS-IGNORE
                    "name": "Parrish, Crosby and Friedman",
                    "status": "active",
                    "type": "commercial",
                },
                "reference_code": f680_reference_code,
                "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "submitted", "value": "Submitted"},
                "submitted_at": submitted_at.isoformat(),
                "submitted_by": None,
            },
            "flags": [],
            "has_advice": {"final": False, "my_team": False, "my_user": False, "team": False, "user": False},
            "id": f680_case_id,
            "latest_activity": None,
            "licences": [],
            "queue_details": [],
            "queue_names": [],
            "queues": [],
            "reference_code": "F680/2025/0000016",
            "sla_days": 0,
            "sla_remaining_days": None,
            "submitted_at": submitted_at.isoformat(),
            "superseded_by": None,
        }
    }


@pytest.fixture
def f680_case_id():
    return "67271217-7e55-4345-9db4-31de1bfe4067"


@pytest.fixture
def f680_reference_code():
    return "F680/2025/0000016"


@pytest.fixture
def queue_f680_cases_to_review():
    return {
        "id": "5641aa2b-09ca-47f6-adcf-682b0472bc93",
        "alias": "F680 Cases to review",
        "name": "F680 Cases to review",
        "is_system_queue": True,
        "countersigning_queue": None,
    }


@pytest.fixture
def mock_f680_case(f680_case_id, requests_mock, data_f680_case):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_post_recommendation(requests_mock, data_f680_case):
    user_recommendation_create_url = f"/cases/{data_f680_case['case']['id']}/user-advice/"
    return requests_mock.post(user_recommendation_create_url, json={}, status_code=201)


@pytest.fixture
def mock_proviso_no_results(requests_mock):
    url = client._build_absolute_uri("/picklist/?type=proviso&page=1&disable_pagination=True&show_deactivated=False")
    return requests_mock.get(url=url, json={"results": []})
