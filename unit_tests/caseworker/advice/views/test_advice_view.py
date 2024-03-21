import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_denial_reasons,
    mock_approval_reason,
    mock_proviso,
    mock_application_good_documents,
):
    yield


@pytest.fixture
def mock_desnz_nuclear_queue(requests_mock):
    data = {
        "id": "00000000-0000-0000-0000-000000000001",
        "alias": "DESNZ_NUCLEAR_CASES_TO_REVIEW",
        "name": "DESNZ Nuclear",
        "is_system_queue": True,
        "countersigning_queue": None,
    }
    url = client._build_absolute_uri("/queues/566fd526-bd6d-40c1-94bd-60d10c967cf7/")
    return requests_mock.get(url=url, json=data)


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:advice_view",
        kwargs={"queue_pk": "566fd526-bd6d-40c1-94bd-60d10c967cf7", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_application(requests_mock):
    def _setup_mock_application(data):
        application_id = data["case"]["id"]
        requests_mock.get(client._build_absolute_uri(f"/cases/{application_id}"), json=data)

    return _setup_mock_application


def test_user_in_context(
    authorized_client,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_user,
    url,
    mock_application,
    assign_user_to_case,
):
    case = data_standard_case_with_all_trigger_list_products_assessed
    mock_application(case)
    assign_user_to_case(
        mock_gov_user,
        case,
    )
    response = authorized_client.get(url)
    # "current_user" passed in from caseworker context processor
    # used to test rule "can_user_change_case"
    assert response.context["current_user"] == mock_gov_user["user"]


def test_advice_view_shows_no_assessed_trigger_list_goods_if_some_are_not_assessed(
    authorized_client,
    url,
    data_standard_case_with_potential_trigger_list_product,
    mock_gov_desnz_nuclear_user,
    mock_application,
    mock_desnz_nuclear_queue,
    mock_gov_user,
    assign_user_to_case,
):
    case = data_standard_case_with_potential_trigger_list_product
    mock_application(case)
    assign_user_to_case(
        mock_gov_user,
        case,
    )

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is None

    make_recommendation_button = soup.find(id="make-recommendation-button")
    assert make_recommendation_button is None


def test_advice_view_shows_assessed_trigger_list_goods_if_all_are_assessed(
    authorized_client,
    requests_mock,
    url,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_desnz_nuclear_user,
    mock_desnz_nuclear_queue,
    mock_application,
    mock_gov_user,
    assign_user_to_case,
):
    case = data_standard_case_with_all_trigger_list_products_assessed
    mock_application(data_standard_case_with_all_trigger_list_products_assessed)
    assign_user_to_case(
        mock_gov_user,
        case,
    )

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is not None

    rows = product_table.tbody.find_all("tr")
    assert len(rows) == len(data_standard_case_with_all_trigger_list_products_assessed["case"]["data"]["goods"])

    make_recommendation_button = soup.find(id="make-recommendation-button")
    assert make_recommendation_button is not None


def test_unallocated_user_does_not_see_assessed_products_or_make_recommendation(
    authorized_client,
    requests_mock,
    url,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_desnz_nuclear_user,
    mock_application,
):
    case = data_standard_case_with_all_trigger_list_products_assessed
    mock_application(case)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is None

    make_recommendation_button = soup.find(id="make-recommendation-button")
    assert make_recommendation_button is None
