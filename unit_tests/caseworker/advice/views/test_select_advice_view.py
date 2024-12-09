import pytest
from bs4 import BeautifulSoup

from django.urls import reverse

from caseworker.advice import services


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:select_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_select_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "recommendation, redirect", [("approve_all", "approve-all-legacy"), ("refuse_all", "refuse-all")]
)
def test_select_advice_post(authorized_client, url, recommendation, redirect, data_standard_case):
    response = authorized_client.post(url, data={"recommendation": recommendation})
    assert response.status_code == 302
    assert (
        response.url
        == f'/queues/00000000-0000-0000-0000-000000000001/cases/{data_standard_case["case"]["id"]}/advice/{redirect}/'
    )


def test_select_advice_post_desnz(authorized_client, url, data_standard_case, mocker):
    get_gov_user_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )
    mocker.patch("caseworker.advice.views.views.get_gov_user", return_value=get_gov_user_value)
    response = authorized_client.post(url, data={"recommendation": "approve_all"})
    assert response.status_code == 302
    assert (
        response.url
        == f'/queues/00000000-0000-0000-0000-000000000001/cases/{data_standard_case["case"]["id"]}/advice/approve-all/'
    )


def test_view_serial_numbers_for_firearm_product_in_select_advice_view(authorized_client, data_standard_case, url):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    assert good_on_application["firearm_details"]["serial_numbers"][0] == "12345"
    assert good_on_application["firearm_details"]["serial_numbers"][1] == "ABC-123"

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_details = [d for d in soup.find_all("details") if "Products" in str(d.summary.span)][0]

    assert "1. 12345" in str(product_details)
    assert "2. ABC-123" in str(product_details)
    assert "Not added yet" not in str(product_details)


def test_serial_numbers_not_added_for_firearm_product_in_select_advice_view(authorized_client, data_standard_case, url):
    data_standard_case["case"]["data"]["goods"][0]["firearm_details"]["serial_numbers"] = []
    data_standard_case["case"]["data"]["goods"][0]["firearm_details"]["serial_numbers_available"] = "LATER"

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_details = [d for d in soup.find_all("details") if "Products" in str(d.summary.span)][0]

    assert "1. 12345" not in str(product_details)
    assert "2. ABC-123" not in str(product_details)
    assert "Not added yet" in str(product_details)


def test_select_advice_get_check_denials(authorized_client, data_standard_case, url):
    denial_match_1 = data_standard_case["case"]["data"]["denial_matches"][0]["denial_entity"]
    denial_match_2 = data_standard_case["case"]["data"]["denial_matches"][1]["denial_entity"]
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    search_input = soup.find_all("p", class_="denial_matches")

    denial_1 = search_input[0]
    assert denial_1.a.get_text(strip=True) == denial_match_1["regime_reg_ref"]
    assert denial_1.span.get_text(strip=True) == "POSSIBLE MATCH"
    id_1 = denial_match_1["id"]
    assert f"/denials/{id_1}" in str(denial_1.a)

    denial_2 = search_input[1]
    assert denial_2.a.get_text(strip=True) == denial_match_2["regime_reg_ref"]
    assert denial_2.span.get_text(strip=True) == "FULL MATCH"
    id_2 = denial_match_2["id"]
    assert f"/denials/{id_2}" in str(denial_2.a)
