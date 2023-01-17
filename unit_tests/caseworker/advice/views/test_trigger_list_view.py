import pytest
from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse

from core import client


@pytest.fixture
def mock_case(requests_mock, data_standard_case_with_potential_trigger_list_product):
    url = client._build_absolute_uri(f"/cases/{data_standard_case_with_potential_trigger_list_product['case']['id']}/")
    return requests_mock.get(url=url, json=data_standard_case_with_potential_trigger_list_product)


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_denial_reasons,
    mock_application_good_documents,
):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:assess_trigger_list", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def advice_url(data_queue, data_standard_case):
    return reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


@pytest.fixture
def edit_assessment_url(data_queue, data_standard_case_with_potential_trigger_list_product):
    application_id = data_standard_case_with_potential_trigger_list_product["case"]["id"]
    good_on_application = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    return reverse(
        "cases:edit_trigger_list",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": application_id,
            "good_on_application_id": good_on_application["id"],
        },
    )


def test_beis_assess_trigger_list_products_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_beis_edit_trigger_list_assessment_before_assessing(authorized_client, edit_assessment_url):
    response = authorized_client.get(edit_assessment_url)
    assert response.status_code == 404


def test_beis_edit_trigger_list_assessment_get(
    authorized_client, edit_assessment_url, data_standard_case_with_potential_trigger_list_product
):
    good_on_application = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    good_on_application["nsg_list_type"] = {"key": "DUAL_USE"}
    good_on_application["is_nca_applicable"] = False
    good_on_application["nsg_assessment_note"] = ""
    data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0] = good_on_application
    response = authorized_client.get(edit_assessment_url)
    assert response.status_code == 200


def test_beis_assess_trigger_list_products_renders_template(authorized_client, url):
    response = authorized_client.get(url)
    assertTemplateUsed(response, "advice/trigger_list_home.html")


def test_beis_assess_trigger_list_products_json(
    authorized_client,
    url,
    data_standard_case_with_potential_trigger_list_product,
):
    unassessed_good = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    response = authorized_client.get(url)
    assert response.context["unassessed_trigger_list_goods_json"] == [
        {"id": unassessed_good["id"], "name": unassessed_good["good"]["name"]}
    ]


def test_beis_assess_trigger_list_products_post_final_advice_and_returns_to_advice_view(
    authorized_client, url, advice_url, requests_mock, data_standard_case_with_potential_trigger_list_product
):
    application_id = data_standard_case_with_potential_trigger_list_product["case"]["id"]
    good_on_application = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    requests_mock.put(f"/applications/{application_id}/goods-on-application/", json={})
    data = {
        "nsg_list_type": "TRIGGER_LIST",
        "is_nca_applicable": True,
        "nsg_assessment_note": "meets criteria",
        "goods": [good_on_application["id"]],
    }
    response = authorized_client.post(url, data=data)

    assert response.status_code == 302
    # All products have been assessed so go to advice page
    assert response.headers["Location"] == advice_url
    assert requests_mock.request_history.pop().json() == [
        {
            "id": good_on_application["id"],
            "application": application_id,
            "good": good_on_application["good"]["id"],
            "nsg_list_type": "TRIGGER_LIST",
            "is_nca_applicable": True,
            "nsg_assessment_note": "meets criteria",
        }
    ]


def test_beis_assess_trigger_list_products_post_advice_and_remains_on_trigger_list_view(
    authorized_client, url, requests_mock, data_standard_case_with_potential_trigger_list_product
):
    application_id = data_standard_case_with_potential_trigger_list_product["case"]["id"]

    good_on_application_1 = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][1]
    good_on_application_2 = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][2]
    del good_on_application_2["nsg_list_type"]
    del good_on_application_2["is_nca_applicable"]

    requests_mock.put(f"/applications/{application_id}/goods-on-application/", json={})
    data = {
        "nsg_list_type": "TRIGGER_LIST",
        "is_nca_applicable": True,
        "nsg_assessment_note": "meets criteria",
        "goods": [good_on_application_1["id"], good_on_application_2["id"]],
    }
    response = authorized_client.post(url, data=data)

    assert response.status_code == 302
    # First product has not been assessed so remain on the trigger list view.
    assert response.headers["Location"] == url


def test_beis_assessed_trigger_list_products(
    authorized_client,
    url,
    data_standard_case_with_potential_trigger_list_product,
):
    trigger_list_product = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][1]
    dual_use_product = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][2]
    response = authorized_client.get(url)
    for good in response.context["assessed_trigger_list_goods"]:
        good.pop("line_number")
    assert response.context["assessed_trigger_list_goods"] == [trigger_list_product, dual_use_product]


def get_cells(soup, table_id):
    return ["\n".join([t.strip() for t in td.text.strip().split("\n")]) for td in soup.find(id=table_id).find_all("td")]


def test_assessed_products_table(authorized_client, url):
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="assessed-products")
    assert get_cells(soup, "assessed-products") == [
        "1.",
        "p2",
        "ML8a,ML9a",
        "Yes",
        "Yes",
        "No",
        "No",
        "",
        "Edit",
        "2.",
        "p2",
        "ML8a,ML9a",
        "Yes",
        "No",
        "Yes",
        "Yes",
        "",
        "Edit",
    ]


@pytest.fixture
def clear_assessments_url(data_queue, data_standard_case):
    return reverse(
        "cases:clear_trigger_list_assessments",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_beis_clear_assessments_trigger_list_products_post(
    authorized_client, clear_assessments_url, requests_mock, data_standard_case_with_potential_trigger_list_product
):
    application_id = data_standard_case_with_potential_trigger_list_product["case"]["id"]
    good_on_application = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    requests_mock.put(f"/applications/{application_id}/goods-on-application/", json={})
    data = {
        "nsg_list_type": "TRIGGER_LIST",
        "is_nca_applicable": True,
        "nsg_assessment_note": "meets criteria",
        "goods": [good_on_application["id"]],
    }
    response = authorized_client.post(clear_assessments_url, data=data)
    assert response.status_code == 302
    requests_mock.request_history.pop().json() == {
        "id": good_on_application["id"],
        "application": application_id,
        "good": good_on_application["good"]["id"],
        "nsg_list_type": "",
        "is_nca_applicable": None,
        "nsg_assessment_note": "",
    }


def test_beis_assess_trigger_list_products_edit(
    authorized_client, edit_assessment_url, requests_mock, data_standard_case_with_potential_trigger_list_product
):
    application_id = data_standard_case_with_potential_trigger_list_product["case"]["id"]
    good_on_application = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]
    good_on_application["nsg_list_type"] = {"key": "DUAL_USE"}
    good_on_application["is_nca_applicable"] = False
    good_on_application["nsg_assessment_note"] = ""
    data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0] = good_on_application

    requests_mock.put(f"/applications/{application_id}/goods-on-application/", json={})
    data = {
        "nsg_list_type": "TRIGGER_LIST",
        "is_nca_applicable": True,
        "nsg_assessment_note": "updated note",
    }
    response = authorized_client.post(edit_assessment_url, data=data)
    assert response.status_code == 302
    assert requests_mock.request_history.pop().json() == [
        {
            "id": good_on_application["id"],
            "application": application_id,
            "good": good_on_application["good"]["id"],
            "nsg_list_type": "TRIGGER_LIST",
            "is_nca_applicable": True,
            "nsg_assessment_note": "updated note",
        }
    ]
