from urllib import parse
import uuid
from django.urls import reverse
import pytest
from core import client
from bs4 import BeautifulSoup


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case_activity_system_user,
    mock_case,
    mock_application_search,
    mock_standard_case_ecju_queries,
):
    yield


@pytest.fixture(autouse=True)
def url(standard_case_pk, queue_pk):
    return reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})


@pytest.fixture(autouse=True)
def denials_data():
    return [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "address": "726 example road",
            "country": "Germany",
            "end_use": 'For the needs of "example company"',
            "item_description": "example something",
            "denial_cle": "FR3a",
            "name": "Example Name",
            "notifying_government": "Lithuania",
            "reference": "Abc123/abc123",
            "regime_reg_ref": "ABC-1234",
            "entity_type": {
                "key": "CONSIGNEE",
                "value": "Consignee",
            },
        }
    ]


@pytest.fixture(autouse=True)
def denials_search_results(denials_data):
    return {
        "count": 1,
        "results": denials_data,
        "total_pages": 1,
    }


@pytest.fixture(autouse=True)
def mock_denials_search(requests_mock, denials_search_results):
    url = client._build_absolute_uri("/external-data/denial-search/")
    return requests_mock.get(url=url, json=denials_search_results)


@pytest.fixture
def denials_search_score_flag_on(settings):
    settings.FEATURE_FLAG_DENIALS_SEARCH_SCORE = True


@pytest.fixture
def denials_search_score_flag_off(settings):
    settings.FEATURE_FLAG_DENIALS_SEARCH_SCORE = False


@pytest.mark.parametrize(
    "party_type",
    (
        "end_user",
        "consignee",
    ),
)
def test_search_denials_party_type(mock_denials_search, party_type, authorized_client, data_standard_case, url):

    party_type_id = data_standard_case["case"]["data"][party_type]["id"]
    party_type_name = data_standard_case["case"]["data"][party_type]["name"]
    party_type_address = data_standard_case["case"]["data"][party_type]["address"]
    party_type_country = data_standard_case["case"]["data"][party_type]["country"]["name"]

    response = authorized_client.get(
        url,
        data={party_type: party_type_id},
    )
    assert response.status_code == 200

    expected_query_params = {
        "search": f"name:({party_type_name}) address:({party_type_address})",
        "page": 1,
        "country": {party_type_country},
    }
    search_url = client._build_absolute_uri("/external-data/denial-search/")
    expected_url = f"{search_url}?{parse.urlencode(expected_query_params, doseq=True, safe=':')}"

    assert mock_denials_search.request_history[0].url == expected_url


@pytest.mark.parametrize(
    "party_type,party_type_data_key",
    (
        ["ultimate_end_user", "ultimate_end_users"],
        ["third_party", "third_parties"],
    ),
)
def test_search_denials_party_type_ultimate_and_third_party(
    mock_denials_search, party_type, party_type_data_key, authorized_client, data_standard_case, url
):

    data_standard_case["case"]["data"][party_type_data_key].append(
        {
            "id": str(uuid.uuid4()),
            "name": "test",
            "address": "55",
            "country": {"name": "United Kingdom"},
        }
    )

    party_users = data_standard_case["case"]["data"][party_type_data_key]
    response = authorized_client.get(url + f"?{party_type}={party_users[0]['id']}&{party_type}={party_users[1]['id']}")
    assert response.status_code == 200

    search_params = f"name:({party_users[0]['name']}) address:({party_users[0]['address']}) name:({party_users[1]['name']}) address:({party_users[1]['address']})"

    expected_query_params = {"search": search_params, "page": 1, "country": {"United Kingdom"}}
    search_url = client._build_absolute_uri("/external-data/denial-search/")
    expected_url = f"{search_url}?{parse.urlencode(expected_query_params, doseq=True, safe=':')}"

    assert mock_denials_search.request_history[0].url == expected_url


@pytest.mark.parametrize(
    "search_string, country_filter",
    (
        ("name:(John Smith) address:(Studio 47v, ferry, town, DD1 4AA)", {"country": ["United Kingdom"]}),  # /PS-IGNORE
        (
            "name:(John Smith) address:(Studio 47v, ferry, town, DD1 4AA) name:(time) address:(2 doc rd)",  # /PS-IGNORE
            {"country": ["United Kingdom"]},
        ),
        ("name:(Smith)", {"country": []}),
    ),
)
def test_search_denials_search_string(
    authorized_client, search_string, country_filter, data_standard_case, mock_denials_search, url
):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    authorized_client.post(
        f"{url}?end_user={end_user_id}",
        data={"search_string": search_string, "country_filter": country_filter["country"]},
    )

    expected_query_params = {"search": search_string, "page": 1, **country_filter}
    search_url = client._build_absolute_uri("/external-data/denial-search/")
    expected_url = f"{search_url}?{parse.urlencode(expected_query_params, doseq=True, safe=':')}"

    assert mock_denials_search.request_history[0].url == expected_url


def test_search_score_feature_flag_on(authorized_client, data_standard_case, url, denials_search_score_flag_on):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    response = authorized_client.get(f"{url}?end_user={end_user_id}")
    soup = BeautifulSoup(response.content, "html.parser")
    search_header = soup.find("th", string="Search score")
    assert search_header


def test_search_denials(
    authorized_client,
    data_standard_case,
    requests_mock,
    standard_case_pk,
    queue_pk,
    denials_data,
    url,
    denials_search_score_flag_off,
):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    end_user_name = data_standard_case["case"]["data"]["end_user"]["name"].replace(" ", "+")
    end_user_address = data_standard_case["case"]["data"]["end_user"]["address"]

    requests_mock.get(
        client._build_absolute_uri(
            f"/external-data/denial-search/?search=name:({end_user_name})+address:({end_user_address})&page=1&country=United+Kingdom"
        ),
        json={"count": "26", "total_pages": "2", "results": denials_data * 26},
    )

    response = authorized_client.get(f"{url}?end_user={end_user_id}")

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find(id="table-denials")
    assert table

    # first tr is headers second onward are data
    row = table.find_all("tr")
    headers = row[0].find_all("th")

    # assert headers
    header_order = [
        "\n",
        "Regime reference",
        "Reference",
        "Name",
        "Address",
        "Country",
        "Denial control list entry",
        "Item description",
        "End use",
        "Party type",
    ]
    header_values = [header.text for header in headers]
    assert header_values == header_order

    # get each column, see that it has data present
    table_body = row[1].find_all("td")[1:]
    table_body_values = [table_values.text.replace("\n", "").strip() for table_values in table_body]
    # maintains order of the table values
    data_key_map = [
        "regime_reg_ref",
        "reference",
        "name",
        "address",
        "country",
        "denial_cle",
        "item_description",
        "end_use",
        "entity_type",
    ]

    expected_table_values = {
        "id": "00000000-0000-0000-0000-000000000001",
        "address": "726 example road",
        "country": "Germany",
        "end_use": 'For the needs of "example company"',
        "item_description": "example something",
        "denial_cle": "FR3a",
        "name": "Example Name",
        "notifying_government": "Lithuania",
        "reference": "Abc123/abc123",
        "regime_reg_ref": "ABC-1234",
        "entity_type": "Consignee",
    }

    for i, value in enumerate(table_body_values):
        assert value == expected_table_values[data_key_map[i]]

    form = soup.find(id="denials-search-form")
    assert form["action"] == f"/queues/{queue_pk}/cases/{standard_case_pk}/denials/?page=1&end_user={end_user_id}"

    page_2 = soup.find(id="page-2")
    assert (
        page_2.button["formaction"]
        == f"/queues/{queue_pk}/cases/{standard_case_pk}/denials/?end_user={end_user_id}&page=2"
    )
    assert page_2.button["form"] == "denials-search-form"


def test_search_denials_no_matches(authorized_client, requests_mock, queue_pk, standard_case_pk):
    requests_mock.get(
        client._build_absolute_uri(f"/external-data/denial-search/"),
        json={"count": 0, "total_pages": 1, "results": []},
    )

    url = reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert response.status_code == 200
    assert "No matching denials" in soup.get_text()


def test_search_denials_query_string_error(authorized_client, requests_mock, queue_pk, data_standard_case, url):
    requests_mock.get(
        client._build_absolute_uri("/external-data/denial-search/?search=%5E%25%24&page=1"),
        json={"errors": {"search": "Invalid search string"}},
    )

    response = authorized_client.post(url, data={"search_string": "^%$"})

    soup = BeautifulSoup(response.content, "html.parser")

    assert response.status_code == 200
    assert "Enter a valid query string" in soup.get_text()


@pytest.fixture
def mock_newline_case(requests_mock, data_standard_case):
    data_standard_case["case"]["data"]["end_user"][
        "address"
    ] = """42\n\r\n\r

Wallaby\r\n\r Way\n

"""
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    yield requests_mock.get(url=url, json=data_standard_case)


def test_search_textarea_newline(
    authorized_client,
    data_standard_case,
    requests_mock,
    standard_case_pk,
    queue_pk,
    denials_data,
    url,
    denials_search_score_flag_off,
    mock_newline_case,
):
    address = "42 \nWallaby \nWay"
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    end_user_name = data_standard_case["case"]["data"]["end_user"]["name"].replace(" ", "+")

    requests_mock.get(
        client._build_absolute_uri(
            f"/external-data/denial-search/?search=name:({end_user_name})+address:({address})&page=1&country=United+Kingdom"
        ),
        json={"count": "26", "total_pages": "2", "results": denials_data * 26},
    )

    response = authorized_client.get(f"{url}?end_user={end_user_id}")

    soup = BeautifulSoup(response.content, "html.parser")
    search_input = soup.find("textarea", id="id_search_string")
    assert search_input
    assert search_input.text == "\nname:(End User) address:(42 Wallaby Way)"
