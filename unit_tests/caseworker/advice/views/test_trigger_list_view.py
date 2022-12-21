import copy
import pytest
from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed
from django.template.loader import render_to_string

from django.urls import reverse

from core import client

from caseworker.advice.enums import NSGListTypes


@pytest.fixture
def data_standard_case_with_potential_trigger_list_product(data_standard_case):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]
    good_on_application["is_good_controlled"] = {"key": "True", "value": "Yes"}
    good_on_application["regime_entries"].append(
        {
            "pk": "abcd976f-fd14-4356-9f23-f6eaf084475d",
            "name": "T1",
            "subsection": {
                "pk": "df3de529-d471-49be-94d7-7a4e5835df90",
                "name": "NSG Potential Trigger List",
                "regime": {
                    "pk": "f990b1c1-a7be-4bc8-9292-a8b5ea25c0dd",
                    "name": "NSG",
                },
            },
        },
    )
    data_standard_case["case"]["data"]["goods"][0] = good_on_application

    # an assessed good on the trigger list
    trigger_list_good = data_standard_case["case"]["data"]["goods"][1]
    trigger_list_good["is_good_controlled"] = {"key": "True", "value": "Yes"}
    trigger_list_good["regime_entries"].append(
        {
            "pk": "abcd976f-fd14-4356-9f23-f6eaf084475d",
            "name": "T1",
            "subsection": {
                "pk": "df3de529-d471-49be-94d7-7a4e5835df90",
                "name": "NSG Potential Trigger List",
                "regime": {
                    "pk": "f990b1c1-a7be-4bc8-9292-a8b5ea25c0dd",
                    "name": "NSG",
                },
            },
        },
    )
    trigger_list_good["nsg_list_type"] = {"key": "TRIGGER_LIST"}
    data_standard_case["case"]["data"]["goods"][1] = trigger_list_good

    # set up another assessed good with different trigger list options
    data_standard_case["case"]["data"]["goods"].append(copy.deepcopy(trigger_list_good))
    data_standard_case["case"]["data"]["goods"][2]["nsg_list_type"] = {"key": "DUAL_USE"}
    data_standard_case["case"]["data"]["goods"][2]["is_nca_applicable"] = True

    return data_standard_case


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


def test_beis_assess_trigger_list_products_get(authorized_client, url):
    response = authorized_client.get(url)
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


def test_beis_assess_trigger_list_products_post(
    authorized_client, url, requests_mock, data_standard_case_with_potential_trigger_list_product
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
    requests_mock.request_history.pop().json() == {
        "id": good_on_application["id"],
        "application": application_id,
        "good": good_on_application["good"]["id"],
        "nsg_list_type": "TRIGGER_LIST",
        "is_nca_applicable": True,
        "nsg_assessment_note": "meets criteria",
    }


def test_beis_assess_trigger_list_products_make_recommandation_not_shown(authorized_client, url):
    response = authorized_client.get(url)
    assert response.context["unassessed_trigger_list_goods"]
    assert response.context["assessed_trigger_list_goods"] == []

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="make-recommendation-button") is None


def test_beis_assess_trigger_list_products_make_recommandation_shown(
    authorized_client, url, mock_case, data_standard_case_with_potential_trigger_list_product
):
    data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][0]["nsg_list_type"] = {
        "key": "TRIGGER_LIST"
    }
    mock_case.return_value = data_standard_case_with_potential_trigger_list_product

    response = authorized_client.get(url)
    assert response.context["unassessed_trigger_list_goods"] == []
    assert response.context["assessed_trigger_list_goods"]

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="make-recommendation-button")


def test_beis_assessed_trigger_list_products(
    authorized_client,
    url,
    data_standard_case_with_potential_trigger_list_product,
):
    trigger_list_product = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][1]
    dual_use_product = data_standard_case_with_potential_trigger_list_product["case"]["data"]["goods"][2]
    response = authorized_client.get(url)
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
        "test assesment note",
        "2.",
        "p2",
        "ML8a,ML9a",
        "Yes",
        "No",
        "Yes",
        "Yes",
        "test assesment note",
    ]
