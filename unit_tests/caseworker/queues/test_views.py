import pytest
import uuid
import re

from bs4 import BeautifulSoup

from django.urls import reverse

import os

from core import client

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"

default_params = {
    "page": ["1"],
    "queue_id": ["00000000-0000-0000-0000-000000000001"],
    "selected_tab": ["all_cases"],
}


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


@pytest.fixture
def mock_team_cases(requests_mock, data_cases_search):
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
        "user": ["Select a user to allocate as Licensing Unit case officer"]
    }


def test_case_assignment_case_office(authorized_client, requests_mock, mock_gov_users):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}"
    )
    case_officer_put_url = client._build_absolute_uri("/cases/cases-update-case-officer/")
    mock_put_case_case_office = requests_mock.put(url=case_officer_put_url, json={})

    data = {"user": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}
    response = authorized_client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("queues:cases", kwargs={"queue_pk": queue_pk})
    assert mock_put_case_case_office.last_request.json() == {
        "gov_user_pk": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb",
        "case_ids": cases_ids,
    }


@pytest.mark.parametrize(
    "user_role_assigned, expected_url_name",
    (
        ("CASE_ADVISOR", "case_assignments"),
        ("LU_CASE_OFFICER", "case_assignments_case_officer"),
    ),
)
def test_case_assignment_select_role(authorized_client, mock_gov_user, user_role_assigned, expected_url_name):
    url_params = f"?cases={str(uuid.uuid4())}&cases={str(uuid.uuid4())}"

    url = reverse("queues:case_assignment_select_role", kwargs={"pk": queue_pk}) + url_params
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, {"role": user_role_assigned})
    assert response.status_code == 302
    assert response.url == reverse(f"queues:{expected_url_name}", kwargs={"pk": queue_pk}) + url_params


def test_with_all_cases_default(authorized_client, mock_cases_search, mock_cases_search_head):

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
            "selected_tab": [tab],
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": ["00000000-0000-0000-0000-000000000001"],
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
        "queue_id": ["00000000-0000-0000-0000-000000000001"],
        "page": ["1"],
        "selected_tab": [tab_name],
        "hidden": ["true"],
    }


@pytest.mark.parametrize(
    "tab_name, tab_id, tab_text",
    [
        ("open_queries", "open-queries-tab", "Open queries"),
        ("my_cases", "my-cases-tab", "My cases"),
    ],
)
def test_tabs_on_team_queue(authorized_client, mock_team_cases, mock_team_queue, tab_name, tab_id, tab_text):
    url = client._build_absolute_uri(f"/queues/{queue_pk}/?selected_tab={tab_name}")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    selected_tab = html.find(id=tab_id)
    all_queries_tab = html.find(id="all-cases-tab")

    assert "Cases to review" in all_queries_tab.get_text()
    assert tab_text in selected_tab.get_text()
    assert f"?selected_tab={tab_name}" in selected_tab.attrs["href"]
    assert "lite-tabs__tab--selected" in selected_tab.attrs["class"]
    assert mock_team_cases.last_request.qs == {
        "queue_id": [queue_pk],
        "page": ["1"],
        "selected_tab": [tab_name],
        "hidden": ["true"],
    }
