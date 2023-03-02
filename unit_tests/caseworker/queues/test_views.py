import pytest
import uuid
import re

from bs4 import BeautifulSoup
from urllib import parse

from django.urls import reverse

import os

from core import client
from core.exceptions import ServiceError

from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS, LU_PRE_CIRC_REVIEW_QUEUE_ALIAS
from caseworker.queues.forms import CaseAssignmentUsersForm, CaseAssignmentQueueForm
from caseworker.queues.views import CaseAssignmentsCaseAssigneeSteps

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"

gov_user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"

default_params = {
    "page": ["1"],
    "queue_id": ["00000000-0000-0000-0000-000000000001"],
    "selected_tab": ["all_cases"],
    "hidden": ["true"],
}

example_return_to_url = "www.example.com"


@pytest.fixture(autouse=True)
def setup(
    mock_cases_search,
    mock_cases_search_head,
    authorized_client,
    queue_pk,
    mock_queue,
    mock_countries,
    mock_queues_list,
    mock_control_list_entries,
    mock_regime_entries,
):
    yield


@pytest.fixture
def data_cases_search(mock_case_statuses, data_case_types, gov_uk_user_id):
    return {
        "count": 1,
        "results": {
            "cases": [
                {
                    "id": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
                    "case_type": {
                        "id": "00000000-0000-0000-0000-000000000001",
                        "reference": {"key": "oiel", "value": "Open Individual Export Licence"},
                        "type": {"key": "application", "value": "Application"},
                        "sub_type": {"key": "open", "value": "Open Licence"},
                    },
                    "destinations": [],
                    "destinations_flags": [],
                    "flags": [
                        {
                            "id": "00000000-0000-0000-0000-000000000007",
                            "name": "Firearms",
                            "colour": "default",
                            "label": None,
                            "priority": 0,
                            "removable_by": "Anyone",
                        },
                        {
                            "id": "00000000-0000-0000-0000-000000000014",
                            "name": "Enforcement Check Req",
                            "colour": "default",
                            "label": None,
                            "priority": 0,
                            "removable_by": "Anyone",
                        },
                    ],
                    "goods_flags": [],
                    "has_open_queries": False,
                    "is_recently_updated": True,
                    "organisation": {},
                    "activity_updates": [
                        {
                            "id": "02cc3048-f893-4f0a-b37f-d066bc0b072a",
                            "created_at": "2023-02-02T17:30:05.184293Z",
                            "user": {
                                "id": "00000000-0000-0000-0000-000000000001",
                                "first_name": "LITE",
                                "last_name": "system",
                                "type": "system",
                                "team": "",
                            },
                            "text": "text line1\r\ntext line2\r\ntext line3\r\ntext line4\r\ntext line5",
                            "additional_text": "additional line1\r\nadditional line2\r\nadditional line3\r\nadditional line4\r\nadditional line5",
                        },
                        {
                            "id": "77d3c3d4-9761-403a-9942-a2fcc41aa35d",
                            "created_at": "2023-02-02T17:30:04.174597Z",
                            "user": {
                                "id": "2eb6e0fa-5a5b-4db1-96cc-dd1473e0c636",
                                "first_name": "Joe",
                                "last_name": "Bloggs",
                                "type": "exporter",
                                "team": "",
                            },
                            "text": "applied for a licence.",
                            "additional_text": "",
                        },
                    ],
                    "assignments": {
                        "9c4e66be-9f0f-451a-9c5f-d30e9c4bb69d": {
                            "email": "test@mail.com",
                            "first_name": "John",
                            "last_name": "Smith",
                            "queues": [{"id": "ee1a3870-73d7-4af3-b629-e28f2c2227d7", "name": "Initial Queue"}],
                            "team_id": "00000000-0000-0000-0000-000000000001",
                            "team_name": "Admin",
                        },
                        "9c4e66be-9f0f-451a-9c5f-d30e9c4bb69e": {
                            "email": "test2@mail.com",
                            "first_name": "Joe",
                            "last_name": "Smith",
                            "queues": [{"id": "ee1a3870-73d7-4af3-b629-e28f2c2227d7", "name": "Initial Queue"}],
                            "team_id": "00000000-0000-0000-0000-000000000001",
                            "team_name": "Admin",
                        },
                    },
                    "queues": [
                        {
                            "countersigning_queue": None,
                            "id": "ee1a3870-73d7-4af3-b629-e28f2c2227d7",
                            "name": "Initial Queue",
                            "team": {
                                "alias": None,
                                "id": "00000000-0000-0000-0000-000000000001",
                                "is_ogd": False,
                                "name": "Admin",
                                "part_of_ecju": False,
                            },
                        },
                        {
                            "countersigning_queue": None,
                            "id": "ee1a3870-73d7-4af3-b629-e28f2c2227d8",
                            "name": "Another Queue",
                            "team": {
                                "alias": None,
                                "id": "00000000-0000-0000-0000-000000000001",
                                "is_ogd": False,
                                "name": "Admin",
                                "part_of_ecju": False,
                            },
                        },
                    ],
                    "case_officer": None,
                    "reference_code": "GBOIEL/2020/0000045/P",
                    "sla_days": 0,
                    "sla_remaining_days": 60,
                    "status": {"key": "submitted", "value": "Submitted"},
                    "next_review_date": None,
                    "licences": [],
                    "submitted_at": "2023-01-16T14:53:09.826340Z",
                },
                {
                    "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                    "case_type": {
                        "id": "00000000-0000-0000-0000-000000000004",
                        "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                        "type": {"key": "application", "value": "Application"},
                        "sub_type": {"key": "standard", "value": "Standard Licence"},
                    },
                    "destinations_flags": [],
                    "flags": [
                        {
                            "id": "00000000-0000-0000-0000-000000000014",
                            "name": "Enforcement Check Req",
                            "alias": "ENF_CHECK_REQ",
                            "colour": "default",
                            "label": None,
                            "priority": 0,
                            "removable_by": "Anyone",
                        }
                    ],
                    "goods_flags": [],
                    "has_open_queries": False,
                    "is_recently_updated": True,
                    "assignments": {},
                    "queues": [],
                    "case_officer": None,
                    "reference_code": "GBSIEL/2020/0002687/T",
                    "sla_days": 2,
                    "sla_remaining_days": 18,
                    "status": {"key": "submitted", "value": "Submitted"},
                    "next_review_date": None,
                    "licences": [],
                    "submitted_at": "2023-01-17T14:53:09.826340Z",
                },
            ],
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
                "gov_users": [
                    {"full_name": "John Smith", "id": gov_uk_user_id, "pending": False},
                    {"full_name": "", "id": gov_uk_user_id, "pending": True},
                ],
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
def mock_cases_search(requests_mock, data_cases_search, queue_pk):
    encoded_params = parse.urlencode({"page": 1, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&{encoded_params}")
    return requests_mock.get(url=url, json=data_cases_search)


@pytest.fixture
def mock_cases_search_page_2(requests_mock, data_cases_search, queue_pk):
    encoded_params = parse.urlencode({"page": 2, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&{encoded_params}")
    return requests_mock.get(url=url, json=data_cases_search)


@pytest.fixture
def mock_cases_search_page_not_found(requests_mock, queue_pk):
    encoded_params = parse.urlencode({"page": 2, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/")
    return requests_mock.get(url=url, status_code=404, json={"errors": {"detail": "Invalid page."}})


@pytest.fixture
def mock_cases_search_error(requests_mock, queue_pk):
    encoded_params = parse.urlencode({"page": 2, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/")
    return requests_mock.get(url=url, status_code=500, json={})


def test_queues_cannot_be_created_and_modified(authorized_client, reset_config_users_list):
    url = reverse("queues:manage")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_queues_can_be_created_and_modified(authorized_client, specify_config_users_list):
    url = reverse("queues:manage")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


@pytest.mark.parametrize(
    "url",
    (
        (reverse("queues:add")),
        (reverse("queues:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_queues_add_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):
    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("queues:add")),
        (reverse("queues:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_queues_add_view_returns_ok_user_on_config_admin_list(authorized_client, specify_config_users_list, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        reverse("core:index"),
        reverse("queues:cases"),
        reverse("queues:cases", kwargs={"queue_pk": "00000000-0000-0000-0000-000000000001"}),
    ],
)
def test_cases_view(url, authorized_client):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.fixture
def mock_enforcement_xml_upload(requests_mock):
    url = client._build_absolute_uri(f"/cases/enforcement-check/{queue_pk}/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_team_queue(requests_mock, data_queue):
    data_queue["is_system_queue"] = False
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


@pytest.fixture()
def mock_queue_with_alias_factory(requests_mock, data_queue):
    def _mock_queue_with_alias(alias):
        data_queue["alias"] = alias
        url = client._build_absolute_uri("/queues/")
        return requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)

    return _mock_queue_with_alias


@pytest.fixture
def mock_team_cases_search(requests_mock, data_cases_search):
    data_cases_search["results"]["filters"]["is_system_queue"] = False
    url = client._build_absolute_uri(f"/cases/")
    yield requests_mock.get(url=url, json=data_cases_search)


@pytest.fixture
def mock_cases_search_head(requests_mock):
    url = client._build_absolute_uri(f"/cases/")
    yield requests_mock.head(url=re.compile(f"{url}.*"), headers={"resource-count": "350"})


@pytest.fixture
def mock_enforcement_xml_validation_error(requests_mock):
    url = client._build_absolute_uri(f"/cases/enforcement-check/{queue_pk}/")
    data = {"errors": {"file": ["Invalid XML format received"]}}
    yield requests_mock.post(url=url, status_code=400, json=data)


def test_upload_enforcement_xml_valid_file(authorized_client, mock_enforcement_xml_upload, settings):
    url = reverse("queues:enforcement_xml_import", kwargs={"pk": queue_pk})

    file_path = os.path.join(settings.BASE_DIR, "unit_tests/caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 302

    with open(file_path, "r") as f:
        assert mock_enforcement_xml_upload.last_request.json() == {"file": f.read()}


def test_upload_enforcement_xml_invalid_file(authorized_client, mock_enforcement_xml_validation_error, settings):
    url = reverse("queues:enforcement_xml_import", kwargs={"pk": queue_pk})

    file_path = os.path.join(settings.BASE_DIR, "unit_tests/caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 200
    assert response.context_data["form"].errors == {"file": ["Invalid XML format received"]}


def test_cases_home_page_view_context(authorized_client):
    context_keys = [
        "sla_radius",
        "sla_circumference",
        "data",
        "queue",
        "filters",
        "is_all_cases_queue",
        "enforcement_check",
        "updated_cases_banner_queue_id",
    ]
    response = authorized_client.get(reverse("queues:cases"))
    assert len(response.context["filters"].filters) == 6
    assert len(response.context["filters"].advanced_filters) == 23
    for context_key in context_keys:
        assert response.context[context_key]
    assert response.status_code == 200


def test_cases_home_page_nca_applicable_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?is_nca_applicable=True"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "is_nca_applicable": ["true"],
    }


def test_cases_home_page_case_search_API_page_not_found(authorized_client, mock_cases_search_page_not_found):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_cases_home_page_case_search_API_error(authorized_client, mock_cases_search_error):
    url = reverse("queues:cases")
    authorized_client.raise_request_exception = True
    with pytest.raises(ServiceError) as exc_info:
        response = authorized_client.get(url)
    exception = exc_info.value
    assert exception.status_code == 502
    assert exception.log_message == "Error retrieving cases data from lite-api"
    assert exception.user_message == "A problem occurred. Please try again later"


def test_cases_home_page_trigger_list_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?is_trigger_list=True"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "is_trigger_list": ["true"],
    }


def test_cases_home_page_regime_entry_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?regime_entry=af8043ee-6657-4d4b-83a2-f1a5cdd016ed"  # /PS-IGNORE
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "regime_entry": ["af8043ee-6657-4d4b-83a2-f1a5cdd016ed"],  # /PS-IGNORE
    }


def test_trigger_list_checkbox_visible_unchecked(authorized_client):
    response = authorized_client.get(reverse("core:index"))
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="is-trigger-list")
    assert "checked" not in checkbox.attrs


def test_trigger_list_checkbox_visible_checked(authorized_client):
    response = authorized_client.get(reverse("core:index") + "/?is_trigger_list=True")
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="is-trigger-list")
    assert "checked" in checkbox.attrs


def test_case_assignment_case_office_no_user_selected(authorized_client, mock_gov_users):
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={str(uuid.uuid4())}&cases={str(uuid.uuid4())}"
    )
    data = {}
    response = authorized_client.post(url, data)

    assert response.status_code == 200
    assert response.context_data["form"].errors == {
        "users": ["Select a user to allocate as Licensing Unit case officer"]
    }


@pytest.fixture
def post_to_step_user_assignment_with_return_to(post_to_step_factory, user_assignment_url):
    user_assignment_url = user_assignment_url + f"&return_to={example_return_to_url}"
    return post_to_step_factory(user_assignment_url)


def test_case_assignment_case_adviser(
    mock_gov_users,
    mock_team_queue,
    mock_put_assignments,
    post_to_step_user_assignment_with_return_to,
):
    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    response = post_to_step_user_assignment_with_return_to(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 302
    assert response.url == example_return_to_url


@pytest.fixture
def mock_put_case_case_officer(requests_mock):
    case_officer_put_url = client._build_absolute_uri("/cases/cases-update-case-officer/")
    return requests_mock.put(url=case_officer_put_url, json={})


def test_case_assignment_case_officer(authorized_client, requests_mock, mock_gov_users, mock_put_case_case_officer):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}"
    )

    data = {"users": gov_user_id}
    response = authorized_client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("queues:cases", kwargs={"queue_pk": queue_pk})
    assert mock_put_case_case_officer.last_request.json() == {
        "gov_user_pk": gov_user_id,
        "case_ids": cases_ids,
    }


def test_case_assignment_case_officer_with_return_to(
    authorized_client, requests_mock, mock_gov_users, mock_put_case_case_officer
):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}&return_to={example_return_to_url}"
    )
    data = {"users": gov_user_id}
    response = authorized_client.post(url, data)
    assert response.status_code == 302
    assert response.url == example_return_to_url


@pytest.mark.parametrize(
    "user_role_assigned, expected_url_name",
    (
        ("CASE_ADVISOR", "case_assignments_assign_user"),
        ("LU_CASE_OFFICER", "case_assignments_case_officer"),
    ),
)
def test_case_assignment_select_role(authorized_client, mock_gov_user, user_role_assigned, expected_url_name):
    url_params = f"?cases={str(uuid.uuid4())}&cases={str(uuid.uuid4())}&return_to={example_return_to_url}"

    url = reverse("queues:case_assignment_select_role", kwargs={"pk": queue_pk}) + url_params
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, {"role": user_role_assigned})
    assert response.status_code == 302
    assert response.url == reverse(f"queues:{expected_url_name}", kwargs={"pk": queue_pk}) + url_params


def test_tabs_with_all_cases_default(authorized_client, mock_cases_search, mock_cases_search_head):
    response = authorized_client.get(reverse("core:index"))
    html = BeautifulSoup(response.content, "html.parser")
    all_queries_tab = html.find(id="all-cases-tab")
    my_cases_tab = html.find(id="my-cases-tab")
    open_queries_tab = html.find(id="open-queries-tab")

    assert "All cases" in all_queries_tab.get_text()
    assert "(350)" in all_queries_tab.get_text()
    assert "My cases" in my_cases_tab.get_text()
    assert "(350)" in my_cases_tab.get_text()
    assert "Open queries" in open_queries_tab.get_text()
    assert "(350)" in open_queries_tab.get_text()
    assert "lite-tabs__tab--selected" in all_queries_tab.attrs["class"]

    head_request_history = [x.qs for x in mock_cases_search_head.request_history]
    assert default_params in head_request_history

    tabs_with_hidden_param = ("my_cases", "open_queries")
    for tab in tabs_with_hidden_param:
        assert {
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": ["00000000-0000-0000-0000-000000000001"],
            "selected_tab": [tab],
        } in head_request_history


def test_tabs_with_all_cases_param(authorized_client, mock_cases_search):
    response = authorized_client.get(reverse("core:index") + "/?selected_tab=all_cases")
    html = BeautifulSoup(response.content, "html.parser")
    all_queries_button = html.find(id="all-cases-tab")
    assert "?selected_tab=all_cases" in all_queries_button.attrs["href"]
    assert "lite-tabs__tab--selected" in all_queries_button.attrs["class"]
    assert mock_cases_search.last_request.qs == default_params


@pytest.mark.parametrize(
    "tab_name, tab_id, tab_text",
    [
        ("open_queries", "open-queries-tab", "Open queries"),
        ("my_cases", "my-cases-tab", "My cases"),
    ],
)
def test_tabs_on_all_cases_queue(authorized_client, mock_cases_search, tab_name, tab_id, tab_text):
    response = authorized_client.get(reverse("core:index") + f"/?selected_tab={tab_name}")
    html = BeautifulSoup(response.content, "html.parser")
    selected_tab = html.find(id=tab_id)
    all_queries_tab = html.find(id="all-cases-tab")

    assert tab_text in selected_tab.get_text()
    assert "All cases" in all_queries_tab.get_text()
    assert f"?selected_tab={tab_name}" in selected_tab.attrs["href"]
    assert "lite-tabs__tab--selected" in selected_tab.attrs["class"]
    assert mock_cases_search.last_request.qs == {
        "hidden": ["true"],
        "page": ["1"],
        "queue_id": ["00000000-0000-0000-0000-000000000001"],
        "selected_tab": [tab_name],
    }


@pytest.mark.parametrize(
    "tab_name, tab_id, tab_text",
    [
        ("open_queries", "open-queries-tab", "Open queries"),
        ("my_cases", "my-cases-tab", "My cases"),
    ],
)
def test_tabs_on_team_queue(
    authorized_client, mock_team_cases_search, mock_team_queue, mock_cases_search_head, tab_name, tab_id, tab_text
):
    url = client._build_absolute_uri(f"/queues/{queue_pk}/?selected_tab={tab_name}")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    selected_tab = html.find(id=tab_id)
    all_cases_tab = html.find(id="all-cases-tab")

    assert "Cases to review" in all_cases_tab.get_text()
    assert tab_text in selected_tab.get_text()
    assert f"?selected_tab={tab_name}" in selected_tab.attrs["href"]
    assert "lite-tabs__tab--selected" in selected_tab.attrs["class"]
    assert mock_team_cases_search.last_request.qs == {
        "hidden": ["true"],
        "page": ["1"],
        "queue_id": [queue_pk],
        "selected_tab": [tab_name],
    }
    head_request_history = [x.qs for x in mock_cases_search_head.request_history]
    assert {
        "hidden": ["false"],
        "page": ["1"],
        "queue_id": [queue_pk],
        "selected_tab": ["all_cases"],
    } in head_request_history

    tabs_with_hidden_param = ("my_cases", "open_queries")
    for tab in tabs_with_hidden_param:
        assert {
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": [queue_pk],
            "selected_tab": [tab],
        } in head_request_history


def test_tabs_on_team_queue_with_hidden_param(
    authorized_client, mock_team_cases_search, mock_team_queue, mock_cases_search_head
):
    url = client._build_absolute_uri(f"/queues/{queue_pk}/?hidden=True")
    authorized_client.get(url)

    assert mock_team_cases_search.last_request.qs == {
        "hidden": ["true"],
        "page": ["1"],
        "queue_id": [queue_pk],
        "selected_tab": ["all_cases"],
    }
    head_request_history = [x.qs for x in mock_cases_search_head.request_history]
    tabs_with_hidden_param = ("all_cases", "my_cases", "open_queries")
    for tab in tabs_with_hidden_param:
        assert {
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": [queue_pk],
            "selected_tab": [tab],
        } in head_request_history


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_case_search_tabs_context(url, authorized_client, mock_cases_search_page_2):
    response = authorized_client.get(url + "?page=2")
    assert response.context["tab_data"] == {
        "all_cases": {"count": "350", "is_selected": True, "url": "?selected_tab=all_cases"},
        "my_cases": {"count": "350", "is_selected": False, "url": "?selected_tab=my_cases"},
        "open_queries": {"count": "350", "is_selected": False, "url": "?selected_tab=open_queries"},
    }


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_queue_assignments(url, authorized_client):
    response = authorized_client.get(url)
    expected_queue_assignments = {
        "ee1a3870-73d7-4af3-b629-e28f2c2227d7": {
            "assignees": [
                {
                    "email": "test@mail.com",
                    "first_name": "John",
                    "last_name": "Smith",
                    "team_id": "00000000-0000-0000-0000-000000000001",
                    "team_name": "Admin",
                },
                {
                    "email": "test2@mail.com",
                    "first_name": "Joe",
                    "last_name": "Smith",
                    "team_id": "00000000-0000-0000-0000-000000000001",
                    "team_name": "Admin",
                },
            ],
            "queue_name": "Initial Queue",
        },
        "ee1a3870-73d7-4af3-b629-e28f2c2227d8": {
            "assignees": [],
            "queue_name": "Another Queue",
        },
    }
    assert response.context["data"]["results"]["cases"][0]["queue_assignments"] == expected_queue_assignments

    html = BeautifulSoup(response.content, "html.parser")
    li_elems = [elem.get_text() for elem in html.find_all("li", {"class": "app-assignments__item"})]
    # first case
    assert "Not allocated" in li_elems[0]
    assert "Licensing Unit case officer" in li_elems[0]
    assert "John Smith" in li_elems[1]
    assert "Initial Queue" in li_elems[1]
    assert "Joe Smith" in li_elems[2]
    assert "Initial Queue" in li_elems[2]
    assert "Not allocated" in li_elems[3]
    assert "Another Queue" in li_elems[3]
    # second case
    assert "Not allocated" in li_elems[4]
    assert "Licensing Unit case officer" in li_elems[4]


@pytest.mark.parametrize(
    "alias",
    (
        (LU_POST_CIRC_FINALISE_QUEUE_ALIAS),
        (LU_PRE_CIRC_REVIEW_QUEUE_ALIAS),
    ),
)
def test_unallocated_assignments_hidden(
    authorized_client, mock_team_cases_search, mock_queue_with_alias_factory, alias
):
    mock_queue_with_alias_factory(alias)
    url = client._build_absolute_uri(f"/queues/{queue_pk}")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    assignments = [elem.get_text() for elem in html.find_all("li", {"class": "app-assignments__item"})]
    assert len(assignments) == 4
    # first case
    assert "Not allocated" in assignments[0]
    assert "Licensing Unit case officer" in assignments[0]
    assert "John Smith" in assignments[1]
    assert "Initial Queue" in assignments[1]
    assert "Joe Smith" in assignments[2]
    assert "Initial Queue" in assignments[2]
    # second case
    assert "Not allocated" in assignments[3]
    assert "Licensing Unit case officer" in assignments[3]


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_activity_updates(url, authorized_client):
    response = authorized_client.get(url)
    expected_activity_updates = [
        {
            "id": "02cc3048-f893-4f0a-b37f-d066bc0b072a",
            "created_at": "2023-02-02T17:30:05.184293Z",
            "user": {
                "id": "00000000-0000-0000-0000-000000000001",
                "first_name": "LITE",
                "last_name": "system",
                "type": "system",
                "team": "",
            },
            "text": "text line1\ntext line2...",
            "additional_text": "additional line1\nadditional line2...",
        },
        {
            "id": "77d3c3d4-9761-403a-9942-a2fcc41aa35d",
            "created_at": "2023-02-02T17:30:04.174597Z",
            "user": {
                "id": "2eb6e0fa-5a5b-4db1-96cc-dd1473e0c636",
                "first_name": "Joe",
                "last_name": "Bloggs",
                "type": "exporter",
                "team": "",
            },
            "text": "applied for a licence.",
            "additional_text": "",
        },
    ]
    assert response.context["data"]["results"]["cases"][0]["activity_updates"] == expected_activity_updates

    html = BeautifulSoup(response.content, "html.parser")
    updates = [update.get_text() for update in html.find_all("li", {"class": "app-updates__item"})]
    assert "LITE system" in updates[0]
    assert "text line1" in updates[0]
    assert "text line2..." in updates[0]
    assert "text line3" not in updates[0]
    assert "additional line1" in updates[0]
    assert "additional line2..." in updates[0]
    assert "additional line3" not in updates[0]
    assert "Joe Bloggs" in updates[1]
    assert "applied for a licence." in updates[1]


def test_case_assignments_add_user_system_queue(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
):

    case = data_standard_case
    url_base = reverse(
        "queues:case_assignments_assign_user",
        kwargs={
            "pk": data_queue["id"],
        },
    )
    url = f"{url_base}?cases={case['case']['id']}"
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentUsersForm)
    # Flow initiated from a system queue, so expect the SELECT_QUEUE step next
    assert context["wizard"]["steps"].next == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Who do you want to allocate as case adviser?" in html.find("h1").get_text()


@pytest.fixture
def mock_users_team_queues_list(requests_mock, gov_uk_user_id, data_queue):
    url = client._build_absolute_uri(f"/users/{gov_uk_user_id}/team-queues/")
    return requests_mock.get(url=url, json={"queues": [[data_queue["id"], "Some Queue"]]})


@pytest.fixture
def user_assignment_url(data_standard_case, data_queue):
    case = data_standard_case
    url_base = reverse("queues:case_assignments_assign_user", kwargs={"pk": data_queue["id"]})
    url = f"{url_base}?cases={case['case']['id']}"
    return url


@pytest.fixture
def post_to_step_user_assignment(post_to_step_factory, user_assignment_url):
    return post_to_step_factory(user_assignment_url)


def test_case_assignments_add_user_system_queue_submit_success(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_users_team_queues_list,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    # POST step 1
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentQueueForm)
    assert context["wizard"]["steps"].current == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Select a team queue to add the case to" in html.find("h1").get_text()

    data = {
        "queue": data_queue["id"],
    }
    # POST step 2
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE,
        data,
        follow=True,
    )
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [gov_user_id],
            }
        ],
        "note": "foobar",
        "remove_existing_assignments": False,
    }

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_assignments_add_user_system_queue_submit_validation_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_users_team_queues_list,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "note": "foobar",
    }
    # POST step 1 - validation error
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["users"].errors == ["Select a user to allocate"]

    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    # POST step 1 - valid
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], CaseAssignmentQueueForm)
    assert response.context["wizard"]["steps"].current == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Select a team queue to add the case to" in html.find("h1").get_text()

    data = {}
    # POST step 2
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["queue"].errors == ["Select a queue to add the case to"]


@pytest.fixture
def mock_team_queue(requests_mock, data_queue):
    data_queue["is_system_queue"] = False
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


@pytest.fixture
def mock_put_assignments(requests_mock, data_queue, data_assignment):
    url = client._build_absolute_uri(f"/queues/{data_queue['id']}/case-assignments/")
    return requests_mock.put(url=url, json=data_assignment)


def test_case_assignments_add_user_team_queue(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_team_queue,
    mock_gov_users,
):

    case = data_standard_case
    url_base = reverse("queues:case_assignments_assign_user", kwargs={"pk": data_queue["id"]})
    url = f"{url_base}?cases={case['case']['id']}"
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentUsersForm)
    # Flow initiated from a team queue, so expect no followup step
    assert context["wizard"]["steps"].next == None

    html = BeautifulSoup(response.content, "html.parser")
    assert "Who do you want to allocate as case adviser?" in html.find("h1").get_text()


def test_case_assignments_add_user_team_queue_submit_success(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_team_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
        follow=True,
    )
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [gov_user_id],
            }
        ],
        "note": "foobar",
        "remove_existing_assignments": False,
    }

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_assignments_add_user_team_queue_submit_validation_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_team_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):

    data = {
        "users": [],
        "note": "foobar",
    }
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["users"].errors == ["Select a user to allocate"]


def test_filter_none_pending_gov_users(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    gov_users = response.context["data"]["results"]["filters"]["gov_users"]
    assert gov_users == [{"full_name": "John Smith", "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0", "pending": False}]
