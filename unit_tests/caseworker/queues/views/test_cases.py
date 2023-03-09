import pytest
import re

from bs4 import BeautifulSoup
from urllib import parse

from django.urls import reverse

from core import client
from core.exceptions import ServiceError

from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS, LU_PRE_CIRC_REVIEW_QUEUE_ALIAS

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"

default_params = {
    "page": ["1"],
    "queue_id": ["00000000-0000-0000-0000-000000000001"],
    "selected_tab": ["all_cases"],
    "hidden": ["true"],
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
                    "email": "test@mail.com",  # /PS-IGNORE
                    "first_name": "John",
                    "last_name": "Smith",
                    "team_id": "00000000-0000-0000-0000-000000000001",
                    "team_name": "Admin",
                },
                {
                    "email": "test2@mail.com",  # /PS-IGNORE
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
            "id": "02cc3048-f893-4f0a-b37f-d066bc0b072a",  # /PS-IGNORE
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
            "id": "77d3c3d4-9761-403a-9942-a2fcc41aa35d",  # /PS-IGNORE
            "created_at": "2023-02-02T17:30:04.174597Z",
            "user": {
                "id": "2eb6e0fa-5a5b-4db1-96cc-dd1473e0c636",  # /PS-IGNORE
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


def test_filter_none_pending_gov_users(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    gov_users = response.context["data"]["results"]["filters"]["gov_users"]
    assert gov_users == [
        {"full_name": "John Smith", "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0", "pending": False}
    ]  # /PS-IGNORE
