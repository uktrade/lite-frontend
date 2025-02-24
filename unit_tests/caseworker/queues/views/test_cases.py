import re
from decimal import Decimal
from urllib import parse

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.core.constants import ADMIN_TEAM_ID, FCDO_TEAM_ID, LICENSING_UNIT_TEAM_ID, TAU_TEAM_ID
from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS, LU_PRE_CIRC_REVIEW_QUEUE_ALIAS
from caseworker.queues.views.forms import CasesFiltersForm
from core import client
from core.exceptions import ServiceError

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"

default_params = {
    "page": ["1"],
    "queue_id": ["00000000-0000-0000-0000-000000000001"],
    "selected_tab": ["all_cases"],
    "hidden": ["true"],
    "sort_by": ["-submitted_at"],
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
    mock_empty_bookmarks,
):
    yield


@pytest.fixture
def mock_cases_search_team_queue(requests_mock, data_cases_search):
    encoded_params = parse.urlencode({"page": 1, "flags": []}, doseq=True)
    url = client._build_absolute_uri(f"/cases/?queue_id={queue_pk}&{encoded_params}")
    return requests_mock.get(url=url, json=data_cases_search)


@pytest.fixture
def mock_team_queue(requests_mock):
    data = {
        "id": queue_pk,
        "alias": None,
        "name": "Some team",
        "is_system_queue": False,
        "countersigning_queue": None,
    }
    url = client._build_absolute_uri("/queues/")
    return requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


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


@pytest.mark.parametrize(
    "url",
    [
        reverse("core:index"),
        reverse("queues:cases"),
        reverse("queues:cases", kwargs={"queue_pk": "00000000-0000-0000-0000-000000000001"}),
    ],
)
def test_cases_view_hidden_user_id(url, mock_gov_user, authorized_client):
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="user_id")["value"] == mock_gov_user["user"]["id"]


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


def test_cases_home_page_view_context(authorized_client):
    context_keys = [
        "sla_radius",
        "sla_circumference",
        "data",
        "queue",
        "is_all_cases_queue",
        "enforcement_check",
    ]
    response = authorized_client.get(reverse("queues:cases"))
    assert isinstance(response.context["form"], CasesFiltersForm)
    expected_fields = [
        "case_reference",
        "export_type",
        "exporter_application_reference",
        "organisation_name",
        "exporter_site_name",
        "goods_starting_point",
        "party_name",
        "max_total_value",
        "control_list_entry",
        "exclude_control_list_entry",
        "regime_entry",
        "exclude_regime_entry",
        "report_summary",
        "submitted_from",
        "submitted_to",
        "finalised_from",
        "finalised_to",
        "exclude_denial_matches",
        "exclude_sanction_matches",
        "status",
        "sub_status",
        "case_officer",
        "assigned_user",
        "licence_status",
        "flags",
        "exclude_flags",
        "countries",
        "assigned_queues",
        "is_nca_applicable",
        "is_trigger_list",
        "return_to",
        "sort_by",
        "product_name",
        "includes_refusal_recommendation_from_ogd",
    ]

    actual_fields = [field_name for field_name, _ in response.context["form"].fields.items()]
    assert set(actual_fields) == set(expected_fields)
    for context_key in context_keys:
        assert response.context[context_key]
    assert not response.context["search_form_has_errors"]
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("query_string", "expected_title"),
    [
        ("", "View all cases in LITE - LITE Internal"),
        ("?selected_tab=all_cases", "View all cases in LITE - LITE Internal"),
        ("?selected_tab=my_cases", "View all cases in LITE - My cases - LITE Internal"),
        ("?selected_tab=open_queries", "View all cases in LITE - Open queries - LITE Internal"),
    ],
)
def test_cases_page_has_correct_title_on_changed_tab(authorized_client, query_string, expected_title):
    response = authorized_client.get(reverse("queues:cases") + query_string)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == expected_title


@pytest.mark.parametrize(
    "url_suffix",
    [
        "",
        "?selected_tab=my_cases",
    ],
)
def test_cases_home_page_view_context_is_filter_visible_hidden(authorized_client, url_suffix):
    response = authorized_client.get(reverse("queues:cases") + url_suffix)
    assert not response.context["is_filters_visible"]


@pytest.mark.parametrize(
    "url_suffix",
    [
        "?case_reference=bar",
        "?a=b",
    ],
)
def test_cases_home_page_view_context_is_filter_visible_visible(authorized_client, url_suffix):
    response = authorized_client.get(reverse("queues:cases") + url_suffix)
    assert response.context["is_filters_visible"]


def test_cases_home_page_post_redirect(authorized_client):
    url = reverse("queues:cases")
    response = authorized_client.post(url, follow=False)
    assert response.url == "/queues/"
    assert response.status_code == 302


def test_case_home_page_invalid_search_form_shows_errors(authorized_client):
    url = reverse("queues:cases")
    response = authorized_client.post(
        url,
        data={
            "status": "madeupstatus",
        },
    )
    assert response.status_code == 200
    assert response.context["search_form_has_errors"]


@pytest.mark.parametrize(
    "form_data",
    [
        {
            "status": "madeupstatus",
        },
        {
            "submitted_from_0": "foo",
        },
    ],
)
def test_case_home_page_invalid_search_form_with_bookmarks_displays_bookmarks(
    authorized_client, mock_bookmarks, form_data
):
    # This is to test against a bug where an invalid form would cause the bookmarks description generation to raise an
    # exception
    url = reverse("queues:cases")
    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.context["bookmarks"] != {"user": []}
    assert response.status_code == 200
    assert response.context["search_form_has_errors"]


def test_cases_home_page_post_redirect_strips_csrftoken(authorized_client):
    url = reverse("queues:cases")
    response = authorized_client.post(url, {"csrfmiddlewaretoken": "foobar", "other_param": "bar"}, follow=False)
    assert response.url == "/queues/?other_param=bar"
    assert response.status_code == 302


def test_cases_home_page_nca_applicable_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?is_nca_applicable=True"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "is_nca_applicable": ["true"],
    }


def test_cases_home_page_return_to_excluded_from_api(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?return_to=foo"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
    }


def test_cases_home_page_assigned_queues(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?assigned_queues=foo"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "assigned_queues": ["foo"],
    }


def test_cases_queue_page_assigned_queues(authorized_client, mock_cases_search_team_queue, mock_team_queue):
    url = reverse("queues:cases", kwargs={"queue_pk": queue_pk}) + "?assigned_queues=foo"
    authorized_client.get(url)
    # Assert that assigned_queues is not sent through to the search API request
    assert mock_cases_search_team_queue.last_request.qs == {
        "page": ["1"],
        "queue_id": [queue_pk],
        "selected_tab": ["all_cases"],
        "hidden": ["false"],
        "sort_by": ["submitted_at"],
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


def test_cases_home_page_control_list_entries_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    control_list_entry_filter_input = html.find(id="control_list_entry")
    cles = [cle.get("value") for cle in control_list_entry_filter_input.findAll("option")]

    assert control_list_entry_filter_input.name == "select"
    assert "ML1" in cles
    assert "ML1a" in cles

    url = reverse("queues:cases") + "?control_list_entry=ML1"
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "control_list_entry": ["ml1"],
    }


def test_cases_home_page_exclude_control_list_entries_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    control_list_entry_filter_input = html.find(id="control_list_entry")
    cles = [cle.get("value") for cle in control_list_entry_filter_input.findAll("option")]

    assert control_list_entry_filter_input.name == "select"
    assert "ML1" in cles
    assert "ML1a" in cles

    url = reverse("queues:cases") + "?control_list_entry=ML1&exclude_control_list_entry=true"
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "control_list_entry": ["ml1"],
        "exclude_control_list_entry": ["true"],
    }


def test_cases_home_page_exclude_flags_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)

    url = reverse("queues:cases") + "?exclude_flags=flag_id_1&exclude_flags=flag_id_2"
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "exclude_flags": ["flag_id_1", "flag_id_2"],
    }


def test_cases_home_page_max_total_value_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    control_list_entry_filter_input = html.find(id="id_max_total_value")
    assert control_list_entry_filter_input.attrs["type"] == "text"
    assert control_list_entry_filter_input.attrs["name"] == "max_total_value"

    url = reverse("queues:cases") + "?max_total_value=300"
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "max_total_value": ["300"],
    }


def test_cases_home_page_goods_starting_point_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    control_list_entry_filter_input = html.find(id="id_goods_starting_point")
    assert control_list_entry_filter_input.attrs["name"] == "goods_starting_point"

    url = reverse("queues:cases") + "?goods_starting_point=NI"
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "goods_starting_point": ["ni"],
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


def test_cases_home_page_exclude_regime_entry_search(authorized_client, mock_cases_search):
    url = (
        reverse("queues:cases")
        + "?regime_entry=af8043ee-6657-4d4b-83a2-f1a5cdd016ed&exclude_regime_entry=true"  # /PS-IGNORE
    )
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "regime_entry": ["af8043ee-6657-4d4b-83a2-f1a5cdd016ed"],  # /PS-IGNORE
        "exclude_regime_entry": ["true"],
    }


def test_cases_home_page_report_summary_matches_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?report_summary=submarines"
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    exclude_denial_matches_input = html.find(id="id_report_summary")
    assert exclude_denial_matches_input.attrs["name"] == "report_summary"
    assert exclude_denial_matches_input.attrs["value"] == "submarines"

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "report_summary": ["submarines"],
    }


def test_cases_home_page_exclude_denial_matches_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?exclude_denial_matches=True"
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    exclude_denial_matches_input = html.find(id="id_exclude_denial_matches")
    assert exclude_denial_matches_input.attrs["name"] == "exclude_denial_matches"

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "exclude_denial_matches": ["true"],
    }


def test_cases_home_page_product_name_matches_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?product_name=submarines"
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    exclude_denial_matches_input = html.find(id="id_product_name")
    assert exclude_denial_matches_input.attrs["name"] == "product_name"
    assert exclude_denial_matches_input.attrs["value"] == "submarines"

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "product_name": ["submarines"],
    }


def test_cases_home_page_exclude_sanction_matches_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?exclude_sanction_matches=True"
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    exclude_sanction_matches_input = html.find(id="id_exclude_sanction_matches")
    assert exclude_sanction_matches_input.attrs["name"] == "exclude_sanction_matches"

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "exclude_sanction_matches": ["true"],
    }


def test_cases_home_page_countries_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?countries=GB&countries=FR"
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    exclude_denial_matches_input = html.find(id="countries")
    assert exclude_denial_matches_input.attrs["name"] == "countries"

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "countries": ["gb", "fr"],
    }


def test_cases_home_page_licence_status_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?licence_status=issued"
    response = authorized_client.get(url)

    assert response.status_code == 200

    html = BeautifulSoup(response.content, "html.parser")

    licence_status_input = str(html.find(id="id_licence_status"))
    assert '<option selected="" value="issued">Issued</option>' in licence_status_input

    assert mock_cases_search.last_request.qs == {
        **default_params,
        "licence_status": ["issued"],
    }


@pytest.mark.parametrize(
    "date_components, expected_output",
    [
        (
            ("1", "1", "23"),
            {
                "submitted_from": ["0023-01-01"],
                "submitted_from_0": ["1"],
                "submitted_from_1": ["1"],
                "submitted_from_2": ["23"],
                "submitted_from_day": ["1"],
                "submitted_from_month": ["1"],
                "submitted_from_year": ["23"],
            },
        ),
        (
            ("01", "01", "2023"),
            {
                "submitted_from": ["2023-01-01"],
                "submitted_from_0": ["01"],
                "submitted_from_1": ["01"],
                "submitted_from_2": ["2023"],
                "submitted_from_day": ["01"],
                "submitted_from_month": ["01"],
                "submitted_from_year": ["2023"],
            },
        ),
    ],
)
def test_cases_home_page_date_search(authorized_client, mock_cases_search, date_components, expected_output):
    day, month, year = date_components
    url = reverse("queues:cases") + f"?submitted_from_0={day}&submitted_from_1={month}&submitted_from_2={year}"
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert mock_cases_search.last_request.qs == {
        **default_params,
        **expected_output,
    }


def test_trigger_list_checkbox_visible_unchecked(authorized_client):
    response = authorized_client.get(reverse("core:index"))
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="id_is_trigger_list")
    assert "checked" not in checkbox.attrs


def test_trigger_list_checkbox_visible_checked(authorized_client):
    response = authorized_client.get(reverse("core:index") + "/?is_trigger_list=True")
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="id_is_trigger_list")
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
            "sort_by": ["-submitted_at"],
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
        "sort_by": ["-submitted_at"],
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
        "sort_by": ["submitted_at"],
    }
    head_request_history = [x.qs for x in mock_cases_search_head.request_history]
    assert {
        "hidden": ["false"],
        "page": ["1"],
        "queue_id": [queue_pk],
        "selected_tab": ["all_cases"],
        "sort_by": ["submitted_at"],
    } in head_request_history

    tabs_with_hidden_param = ("my_cases", "open_queries")
    for tab in tabs_with_hidden_param:
        assert {
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": [queue_pk],
            "selected_tab": [tab],
            "sort_by": ["submitted_at"],
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
        "sort_by": ["submitted_at"],
    }
    head_request_history = [x.qs for x in mock_cases_search_head.request_history]
    tabs_with_hidden_param = ("all_cases", "my_cases", "open_queries")
    for tab in tabs_with_hidden_param:
        assert {
            "hidden": ["true"],
            "page": ["1"],
            "queue_id": [queue_pk],
            "selected_tab": [tab],
            "sort_by": ["submitted_at"],
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


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_context_goods_summary(url, authorized_client):
    response = authorized_client.get(url)
    expected_goods_summary = {
        "cles": {"ML2a", "ML1", "ML2", "ML1a"},
        "regimes": {"Wassenaar Arrangement"},
        "report_summaries": {"prefix subject"},
        "total_value": Decimal("40.00"),
    }
    assert response.context["data"]["results"]["cases"][0]["goods_summary"] == expected_goods_summary


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_context_goods(url, authorized_client):
    response = authorized_client.get(url)
    expected_goods = [
        {
            "cles": ["ML1", "ML1a"],
            "name": "Some product",
            "quantity": "20.00",
            "regimes": ["Wassenaar Arrangement"],
            "report_summary_prefix": "prefix",
            "report_summary_subject": "subject",
            "value": "10.00",
        },
        {
            "cles": ["ML2", "ML2a", "ML1a"],
            "name": "Some other product",
            "quantity": "1.00",
            "regimes": ["Wassenaar Arrangement"],
            "report_summary_prefix": "prefix",
            "report_summary_subject": "subject",
            "value": "30.00",
        },
    ]
    assert response.context["data"]["results"]["cases"][0]["goods"] == expected_goods


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_context_denials(url, authorized_client):
    response = authorized_client.get(url)
    expected_denials = [
        {"address": "some address", "category": "exact", "name": "denial name", "reference": "denialref"},
        {"address": "some address 2", "category": "exact", "name": "denial 2 name", "reference": "denial2ref"},
    ]
    assert response.context["data"]["results"]["cases"][0]["denials"] == expected_denials


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_context_ecju_queries(url, authorized_client):
    response = authorized_client.get(url)
    expected_ecju_queries = [
        {
            "query_type": "query",
            "question": "some question",
            "raised_by_user": "foo bar",
            "responded_by_user": None,
            "response": None,
            "is_query_closed": False,
        },
        {
            "query_type": "query",
            "question": "some other question",
            "raised_by_user": "some user",
            "responded_by_user": "some responder",
            "response": "some response",
            "is_query_closed": True,
        },
    ]
    assert response.context["data"]["results"]["cases"][0]["ecju_queries"] == expected_ecju_queries


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_products(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    products = html.find_all("ol", {"class": "app-products__list"})[0].get_text().strip()
    assert "Some product (20)" in products
    assert "Some other product (1)" in products


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_cles(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    cles = html.find_all("ol", {"class": "app-cles__list"})[0].get_text().strip()
    assert "ML1" in cles
    assert "ML1a" in cles
    assert "ML2" in cles
    assert "ML2a" in cles


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_report_summaries(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    report_summaries = html.find_all("ol", {"class": "app-report-summaries__list"})[0].get_text().strip()
    assert "prefix subject" in report_summaries


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_regimes(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    regimes = html.find_all("ol", {"class": "app-regimes__list"})[0].get_text().strip()
    assert "Wassenaar Arrangement" in regimes


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_total_value(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    total_value = html.find_all("span", {"class": "app-total-value"})[0].get_text().strip()
    assert "£40.00" in total_value


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_queries(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    queries = html.find_all("span", {"class": "app-ecju-queries"})[0].get_text().strip()
    assert "2 queries" in queries


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_denials(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    denials = html.find_all("span", {"class": "app-denials"})[0].get_text().strip()
    assert "2 denials" in denials


@pytest.mark.parametrize(
    "url",
    (
        (reverse("core:index")),
        (reverse("queues:cases")),
    ),
)
def test_column_intended_end_use(url, authorized_client):
    response = authorized_client.get(url)

    html = BeautifulSoup(response.content, "html.parser")
    intended_end_use = html.find_all("span", {"class": "app-intended-end-use"})[0].get_text().strip()
    assert "birthday present" in intended_end_use


def test_filter_none_pending_gov_users(authorized_client, mock_cases_search):
    url = reverse("queues:cases")
    response = authorized_client.get(url)
    gov_users = response.context["data"]["results"]["filters"]["gov_users"]
    assert gov_users == [
        {"full_name": "John Smith", "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0", "pending": False}  # /PS-IGNORE
    ]


def test_cases_home_page_return_to_search(authorized_client, mock_cases_search):
    regime_entry = "af8043ee-6657-4d4b-83a2-f1a5cdd016ed"  # /PS-IGNORE
    url = reverse("queues:cases") + f"?regime_entry={regime_entry}&return_to=/foobar"
    response = authorized_client.get(url)
    # Ensure return_to not sent in server call
    assert mock_cases_search.last_request.qs == {
        **default_params,
        "regime_entry": [regime_entry],
    }
    # Ensure return_to parameter does not appear in return_to url value
    assert response.context["return_to"] == f"/queues/?regime_entry={regime_entry}"


def test_case_row_sub_status(
    authorized_client,
):
    response = authorized_client.get(reverse("core:index"))

    html = BeautifulSoup(response.content, "html.parser")
    sub_status = html.find(string=re.compile("test sub status"))
    assert sub_status == "test sub status"


@pytest.mark.parametrize(
    ("mock_gov_user_team", "expected"),
    (
        ({"id": ADMIN_TEAM_ID, "name": "Admin", "alias": None}, True),
        ({"id": TAU_TEAM_ID, "name": "TAU", "alias": "TAU"}, True),
        ({"id": FCDO_TEAM_ID, "name": "FCDO", "alias": "FCO"}, False),
        ({"id": LICENSING_UNIT_TEAM_ID, "name": "Licensing Unit", "alias": "LICENSING_UNIT"}, False),
    ),
)
def test_product_search_is_visible_to_specific_users_only(
    authorized_client, requests_mock, mock_gov_user, gov_uk_user_id, mock_gov_user_team, expected
):
    mock_gov_user["user"]["team"] = mock_gov_user_team
    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)

    response = authorized_client.get(reverse("queues:cases"))
    soup = BeautifulSoup(response.content, "html.parser")
    is_product_search_visible = "Search for products" in str(soup.find(id="link-product-search"))
    assert is_product_search_visible == expected


def test_queue_view_sort_params_persist(authorized_client):
    response = authorized_client.get(reverse("core:index"))
    assert response.status_code == 200
    assert authorized_client.session["case_search_sort_by"] == "-submitted_at"

    authorized_client.get(reverse("core:index") + "?sort_by=submitted_at")
    assert response.status_code == 200
    assert authorized_client.session["case_search_sort_by"] == "submitted_at"
