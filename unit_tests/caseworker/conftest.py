import re
import os
from urllib import parse

import pytest
from dotenv import load_dotenv
from django.test import Client

from core import client
from core.helpers import convert_value_to_query_param
from caseworker.advice.services import LICENSING_UNIT_TEAM

application_id = "094eed9a-23cc-478a-92ad-9a05ac17fad0"
second_application_id = "08e69b60-8fbd-4111-b6ae-096b565fe4ea"
gov_uk_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"


DEFAULT_ENVFILE = "caseworker.env"


def pytest_configure(config):
    """
    Load caseworker env variables automagically
    """
    if not os.environ.get("PIPENV_DOTENV_LOCATION"):
        load_dotenv(dotenv_path=DEFAULT_ENVFILE, override=True)


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
def data_cases_search(data_open_case, data_standard_case, mock_case_statuses, data_case_types):
    return {
        "count": 2,
        "results": {
            "cases": [data_open_case["case"], data_standard_case["case"]],
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
def open_case_pk(data_open_case):
    return data_open_case["case"]["id"]


@pytest.fixture
def standard_case_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def mock_open_case(requests_mock, data_open_case):
    url = client._build_absolute_uri(f"/cases/{data_open_case['case']['id']}/")
    yield requests_mock.get(url=url, json=data_open_case)


@pytest.fixture
def mock_standard_case(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    yield requests_mock.get(url=url, json=data_standard_case)


@pytest.fixture
def mock_case(
    mock_case_ecju_queries,
    mock_case_assigned_queues,
    mock_case_documents,
    mock_case_additional_documents,
    mock_case_activity_filters,
    mock_open_case,
    mock_standard_case,
):
    yield


@pytest.fixture
def mock_all_standard_case_data(
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_documents,
    mock_standard_case_activity_filters,
    mock_get_standard_case_activity,
):
    yield


@pytest.fixture
def data_queue():
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "All cases",
        "is_system_queue": True,
        "countersigning_queue": None,
    }


@pytest.fixture
def stub_response():
    return {}


@pytest.fixture
def stub_case_activity():
    return {"activity": {}}


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
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin", "alias": None},
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
def mock_standard_case_ecju_queries(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries/")
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
def mock_standard_case_assigned_queues(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/assigned-queues/")
    data = {"queues": []}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_denial_reasons(requests_mock):
    url = client._build_absolute_uri("/static/denial-reasons/")
    data = {
        "denial_reasons": [
            {"id": "1", "display_value": "one", "deprecated": False},
            {"id": "1a", "display_value": "one a", "deprecated": False},
            {"id": "2", "display_value": "two", "deprecated": False},
            {"id": "2a", "display_value": "two a", "deprecated": False},
            {"id": "2b", "display_value": "two b", "deprecated": False},
            {"id": "3", "display_value": "two", "deprecated": False},
            {"id": "4", "display_value": "two", "deprecated": False},
            {"id": "5", "display_value": "two", "deprecated": False},
            {"id": "5a", "display_value": "five a", "deprecated": False},
            {"id": "5b", "display_value": "five b", "deprecated": False},
            {"id": "M", "display_value": "MMMM", "deprecated": False},
        ]
    }
    yield requests_mock.get(url=url, json=data)


@pytest.fixture
def mock_post_refusal_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/user-advice/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture
def current_user():
    return {
        "email": "test.user@example.com",
        "first_name": "Test",
        "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "00000000-0000-0000-0000-000000000001",
            "alias": None,
            "is_ogd": False,
            "name": "Admin",
            "part_of_ecju": None,
        },
    }


@pytest.fixture
def team1_user():
    return {
        "email": "team1.user@example.com",
        "first_name": "Team1 Test",
        "id": "9123453c-e938-4d4f-a71b-12345678e855",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "12345678-42c8-499f-a58d-94f945411234",
            "name": "Team1",
            "alias": "TEAM1",
            "part_of_ecju": True,
            "is_ogd": False,
        },
    }


@pytest.fixture
def MOD_team1_user():
    return {
        "email": "mod.team1@example.com",
        "first_name": "MoD Team1",
        "id": "6543213c-e938-4d4f-a71b-12345678e855",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "2e5fab3c-4599-432e-9540-74ccfafb18ee",
            "name": "MoD Team1",
            "alias": "MOD_DI",
            "part_of_ecju": False,
            "is_ogd": True,
        },
    }


@pytest.fixture
def MOD_team2_user():
    return {
        "email": "mod.team2@example.com",
        "first_name": "MoD Team2",
        "id": "4523453c-e938-4d4f-a71b-12345678e855",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "809eba0f-f197-4f0f-949b-9af309a844fb",
            "name": "MoD Team2",
            "alias": "MOD_DSTL",
            "part_of_ecju": False,
            "is_ogd": True,
        },
    }


@pytest.fixture
def MOD_ECJU_team_user():
    return {
        "email": "mod.ecju.team@example.com",
        "first_name": "MoD ECJU",
        "id": "9123453c-e938-4d4f-a71b-12345678e855",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "b7640925-2577-4c24-8081-b85bd635b62a",
            "name": "MoD ECJU",
            "alias": "MOD_ECJU",
            "part_of_ecju": False,
            "is_ogd": True,
        },
    }


@pytest.fixture
def FCDO_team_user():
    return {
        "email": "fcdo.team@example.com",
        "first_name": "FCDO Team",
        "id": "123453c-e938-4d4f-a71b-12345678e8559",
        "last_name": "User",
        "role_name": "Super User",
        "status": "Active",
        "team": {
            "id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74",
            "name": "FCDO Team",
            "alias": "FCO",
            "part_of_ecju": False,
            "is_ogd": True,
        },
    }


@pytest.fixture
def refusal_advice(current_user):
    return [
        {
            "id": "5cf3c92d-e841-4b8a-8ce5-bd7f869a3e8d",
            "text": "Not matching the criteria to issue the licence",
            "note": None,
            "type": {"key": "refuse", "value": "Refuse"},
            "level": "user",
            "proviso": None,
            "denial_reasons": ["5a", "5b"],
            "footnote": None,
            "user": current_user,
            "created_at": "2021-10-17T23:23:30.421294+01:00",
            "good": "73152304-6026-4cc0-a3d7-0a93048ecdce",
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
        }
    ]


@pytest.fixture
def advice_for_countersign(current_user):
    return [
        {
            "consignee": None,
            "country": None,
            "created_at": "2021-07-14T15:20:35.713348+01:00",
            "denial_reasons": [],
            "end_user": None,
            "footnote": None,
            "good": "de385241-ffe3-4e81-96a6-64c0934bc4e2",
            "goods_type": None,
            "id": "825bddc9-4e6c-4a26-8231-9c0500b037a6",
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "",
            "third_party": None,
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": {
                "email": "yscott@bob-scott.com",
                "first_name": "Scott",
                "id": "5d36079b-e921-4598-b0f9-d7a62da6e9ef",
                "last_name": "Bob",
                "role_name": "Adviser",
                "status": "Active",
                "team": {
                    "id": "2e5fab3c-4599-432e-9540-74ccfafb18ee",
                    "is_ogd": False,
                    "name": "Team-A",
                    "alias": None,
                    "part_of_ecju": False,
                },
            },
        },
        {
            "id": "b32d7dfa-a90d-4b37-adac-db231d4b83be",
            "consignee": None,
            "country": None,
            "created_at": "2021-07-15T13:46:42.608237+01:00",
            "denial_reasons": [],
            "end_user": "095774f4-4e3d-41f0-bfdf-d442ced2933b",
            "footnote": None,
            "good": None,
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "ammunition for Police intended for training use, I recommend issue as it meets the criteria",
            "third_party": None,
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": {
                "email": "robert45@bob-perkins.biz",
                "first_name": "Bob",
                "id": "60bcedcb-ead4-4601-b2d5-e50cbdc7ff31",
                "last_name": "Smith",
                "role_name": "Administrator",
                "status": "Active",
                "team": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "is_ogd": False,
                    "name": "TeamB",
                    "alias": None,
                    "part_of_ecju": True,
                },
            },
        },
        {
            "id": "c9a96d84-6a6b-421d-bbbb-b12b9577d46e",
            "consignee": "64ab5d25-2067-4f37-9593-5dba2707887e",
            "country": None,
            "created_at": "2021-07-15T13:46:42.622782+01:00",
            "denial_reasons": [],
            "end_user": None,
            "footnote": None,
            "good": None,
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "ammunition for Police intended for training use, recommend issue as it meets the criteria",
            "third_party": None,
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": {
                "email": "robert45@bob-perkins.biz",
                "first_name": "Bob",
                "id": "60bcedcb-ead4-4601-b2d5-e50cbdc7ff31",
                "last_name": "Smith",
                "role_name": "Administrator",
                "status": "Active",
                "team": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "is_ogd": False,
                    "name": "TeamB",
                    "alias": None,
                    "part_of_ecju": True,
                },
            },
        },
    ]


@pytest.fixture
def standard_case_with_advice(current_user):
    return {
        "id": "2c14d003-1234-4c11-a0fd-bbfd7572c5a4",
        "data": {
            "goods": [
                {
                    "application": "2c14d003-bdbe-4c11-a0fd-bbfd7572c5a4",
                    "control_list_entries": [
                        {
                            "id": "9622ee4e-3f3a-4f3d-ac5f-08280c9e81c9",
                            "rating": "ML6b1",
                            "text": "clc entry description",
                        }
                    ],
                    "created_at": "2021-09-28T16:01:14.707454+01:00",
                    "good": {
                        "comment": None,
                        "control_list_entries": [
                            {
                                "id": "9622ee4e-3f3a-4f3d-ac5f-08280c9e81c9",
                                "rating": "ML6b1",
                                "text": "clc entry description",
                            }
                        ],
                        "description": "Pair of shotgun barrels",
                        "is_good_controlled": {"key": "True", "value": "Yes"},
                        "name": "Pair of shotgun barrels",
                    },
                    "id": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
                    "is_good_controlled": {"key": "True", "value": "Yes"},
                    "is_good_incorporated": True,
                    "quantity": 2.0,
                    "report_summary": "firearms",
                    "unit": {"key": "NAR", "value": "Number of articles"},
                    "value": "13800.00",
                },
                {
                    "application": "2c14d003-bdbe-4c11-a0fd-bbfd7572c5a4",
                    "control_list_entries": [],
                    "created_at": "2021-09-28T16:03:09.172821+01:00",
                    "good": {
                        "comment": None,
                        "control_list_entries": [],
                        "description": "Pair of shotgun barrels",
                        "is_good_controlled": {"key": "True", "value": "Yes"},
                        "name": "Pair of shotgun barrels 12 bore",
                        "report_summary": None,
                    },
                    "id": "d4feac1e-851d-41a5-b833-eb28addb8547",
                    "is_good_controlled": {"key": "False", "value": "No"},
                    "report_summary": "firearms",
                    "unit": {"key": "NAR", "value": "Number of articles"},
                    "value": "6900.00",
                },
            ]
        },
        "advice": [
            {
                "consignee": None,
                "country": None,
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "denial_reasons": [],
                "end_user": None,
                "footnote": "footnotes",
                "good": "73152304-6026-4cc0-a3d7-0a93048ecdce",
                "id": "429c5596-fe8b-4540-988b-c37805cd08de",
                "level": "user",
                "note": "additional notes",
                "proviso": "no conditions",
                "text": "meets the criteria",
                "third_party": None,
                "type": {"key": "proviso", "value": "Proviso"},
                "ultimate_end_user": None,
                "user": current_user,
            }
        ],
    }


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
def mock_standard_case_documents(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/documents/")
    data = {
        "documents": [
            {
                "id": "c58f84b2-6925-4aee-9888-c3115e2fdc26",
                "name": "Application Form - 2020-08-03 12:52:37.977275+00:00.pdf",
                "type": {"key": "AUTO_GENERATED", "value": "Auto Generated"},
                "metadata_id": "c58f84b2-6925-4aee-9888-c3115e2fdc26",
                "user": None,
                "size": None,
                "case": standard_case_pk,
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
def mock_standard_case_additional_documents(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/additional-contacts/")
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


@pytest.fixture
def mock_standard_case_activity_system_user(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/activity/")
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


@pytest.fixture
def mock_standard_case_activity_filters(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/activity/filters/")
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
            "blocks_finalising": True,
            "removable_by": "Anyone",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin", "alias": None},
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
def good_on_application_pk(data_good_on_application):
    return data_good_on_application["id"]


@pytest.fixture
def mock_good_on_appplication(requests_mock, mock_case, data_good_on_application):
    url = client._build_absolute_uri("/applications/good-on-application")
    yield requests_mock.get(url=re.compile(f"{url}.*"), json=data_good_on_application)


@pytest.fixture
def mock_good_on_appplication_documents(requests_mock, mock_case, data_good_on_application):
    pk = data_good_on_application["application"]
    good_pk = data_good_on_application["good"]["id"]
    url = client._build_absolute_uri(f"/applications/{pk}/goods/{good_pk}/documents/")
    yield requests_mock.get(url=re.compile(f"{url}.*"), json={"documents": []})


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
def mock_application_search(requests_mock, data_search):
    url = client._build_absolute_uri("/search/application/search/")
    yield requests_mock.get(url=url, json=data_search)


@pytest.fixture(autouse=True)
def mock_product_search(requests_mock, data_search):
    url = client._build_absolute_uri("/search/product/search/")
    yield requests_mock.get(url=url, json=data_search)


@pytest.fixture(autouse=True)
def mock_product_more_like_this(requests_mock, data_search):
    url = client._build_absolute_uri("/search/product/more-like-this/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_search)


@pytest.fixture(autouse=True)
def mock_put_flags(requests_mock, stub_response):
    url = client._build_absolute_uri("/flags/assign/")
    yield requests_mock.put(url=url, json=stub_response), 200


@pytest.fixture(autouse=True)
def mock_get_activity(requests_mock, open_case_pk, stub_case_activity):
    url = f"/cases/{open_case_pk}/activity/"
    url = client._build_absolute_uri(url)
    yield requests_mock.get(url=url, json=stub_case_activity)


@pytest.fixture()
def mock_get_standard_case_activity(requests_mock, standard_case_pk, stub_case_activity):
    url = f"/cases/{standard_case_pk}/activity/"
    url = client._build_absolute_uri(url)
    yield requests_mock.get(url=url, json=stub_case_activity)


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
        session["email"] = user["email"]
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


approve = {"key": "approve", "value": "Approve"}
refuse = {"key": "refuse", "value": "Refuse"}
advice_template = {
    "id": "012345678-0123-0123-0123-0123456789abc",
    "text": "Lorem ipsum.",
    "note": "Consectetur adipisicing elit.",
    "type": None,
    "level": "user",
    "proviso": None,
    "denial_reasons": None,
    "footnote": None,
    "user": None,
    "created_at": "2021-10-13T11:30:15.409500+01:00",
    "good": None,
    "goods_type": None,
    "country": None,
    "end_user": None,
    "ultimate_end_user": None,
    "consignee": None,
    "third_party": None,
}


@pytest.fixture
def team1():
    return {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "A team", "part_of_ecju": None, "alias": None}


@pytest.fixture
def team2():
    return {"id": "0017ed1f-390b-4f78-bfca-86300edec300", "name": "B team", "part_of_ecju": None, "alias": None}


@pytest.fixture
def john_smith(team1):
    return {
        "email": "john.smith@example.com",
        "first_name": "John",
        "id": "63c74ddd-c119-48cc-8696-d196218ca583",
        "last_name": "Smith",
        "role_name": "Super User",
        "status": "Active",
        "team": team1,
    }


@pytest.fixture
def jane_doe(team2):
    return {
        "email": "jane.doe@example.com",
        "first_name": "Jane",
        "id": "11c74ddd-c119-48cc-8696-e096218ca583",
        "last_name": "Doe",
        "role_name": "Super User",
        "status": "Active",
        "team": team2,
    }


@pytest.fixture
def end_user_advice1(data_standard_case, john_smith):
    end_user_advice1 = {**advice_template}
    end_user_advice1["id"] = "6cecd825-0582-46e8-b253-4d52a8db3b24"
    end_user_advice1["type"] = approve
    end_user_advice1["user"] = john_smith
    end_user_advice1["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]
    return end_user_advice1


@pytest.fixture
def end_user_advice2(data_standard_case, jane_doe):
    end_user_advice2 = {**advice_template}
    end_user_advice2["id"] = "257c7265-acf8-4bb8-99e3-77142b1b479d"
    end_user_advice2["type"] = approve
    end_user_advice2["user"] = jane_doe
    end_user_advice2["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]
    return end_user_advice2


@pytest.fixture
def consignee_advice1(data_standard_case, john_smith):
    consignee_advice1 = {**advice_template}
    consignee_advice1["id"] = "bce1444f-1d56-40e7-8316-ab1d16afd55d"
    consignee_advice1["type"] = approve
    consignee_advice1["user"] = john_smith
    consignee_advice1["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]
    return consignee_advice1


@pytest.fixture
def consignee_advice2(data_standard_case, jane_doe):
    consignee_advice2 = {**advice_template}
    consignee_advice2["id"] = "d0eeacbb-e33e-4889-bb3a-0e314647597f"
    consignee_advice2["type"] = approve
    consignee_advice2["user"] = jane_doe
    consignee_advice2["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]
    return consignee_advice2


@pytest.fixture
def third_party_advice1(data_standard_case, john_smith):
    third_party_advice1 = {**advice_template}
    third_party_advice1["id"] = "34365628-d9cf-443f-a34c-362507141be1"
    third_party_advice1["type"] = refuse
    third_party_advice1["user"] = john_smith
    third_party_advice1["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]
    return third_party_advice1


@pytest.fixture
def third_party_advice2(data_standard_case, jane_doe):
    third_party_advice2 = {**advice_template}
    third_party_advice2["id"] = "0ac9eb9a-f9ea-4abd-8c97-9e5113a7ca97"
    third_party_advice2["type"] = approve
    third_party_advice2["user"] = jane_doe
    third_party_advice2["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]
    return third_party_advice2


@pytest.fixture
def goods_advice1(data_standard_case, john_smith):
    goods_advice1 = {**advice_template}
    goods_advice1["id"] = "34365628-d9cf-443f-a34c-362507141be1"
    goods_advice1["type"] = refuse
    goods_advice1["user"] = john_smith
    goods_advice1["good"] = data_standard_case["case"]["data"]["goods"][0]["id"]
    return goods_advice1


@pytest.fixture
def goods_advice2(data_standard_case, jane_doe):
    goods_advice2 = {**advice_template}
    goods_advice2["id"] = "0ac9eb9a-f9ea-4abd-8c97-9e5113a7ca97"
    goods_advice2["type"] = approve
    goods_advice2["user"] = jane_doe
    goods_advice2["good"] = data_standard_case["case"]["data"]["goods"][0]["id"]
    return goods_advice2


@pytest.fixture
def form_team_data():
    return {
        "name": "Test",
        "part_of_ecju": True,
        "is_ogd": True,
    }


@pytest.fixture
def mock_precedents_api(requests_mock, data_standard_case, data_queue):
    case_id = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/cases/{case_id}/good-precedents/")
    requests_mock.get(
        url,
        json={
            "results": [
                {
                    "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "application": case_id,
                    "queue": data_queue["id"],
                    "reference": data_standard_case["case"]["reference_code"],
                    "destinations": ["GB"],
                    "control_list_entries": ["ML1a"],
                    "wassenaar": False,
                    "quantity": 10.0,
                    "value": "test-value",
                    "report_summary": "test-report-summary",
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "application": case_id,
                    "queue": data_queue["id"],
                    "reference": data_standard_case["case"]["reference_code"],
                    "destinations": ["GB"],
                    "control_list_entries": ["ML1a"],
                    "wassenaar": False,
                    "quantity": 10.0,
                    "value": "test-value",
                    "report_summary": "test-report-summary",
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ]
        },
    )
    return requests_mock
