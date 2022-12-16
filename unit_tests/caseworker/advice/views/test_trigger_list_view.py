import pytest
import re

from django.urls import reverse


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

    return data_standard_case


def test_beis_assess_trigger_list_products_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


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
