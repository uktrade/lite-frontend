from unittest import mock

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client
from caseworker.advice import services


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_case):
    yield


@pytest.fixture
def data_case_advice(
    data_standard_case,
    end_user_advice1,
    end_user_advice2,
    consignee_advice1,
    consignee_advice2,
    third_party_advice1,
    third_party_advice2,
    goods_advice1,
    goods_advice2,
):
    return [
        end_user_advice1,
        end_user_advice2,
        consignee_advice1,
        consignee_advice2,
        third_party_advice1,
        third_party_advice2,
        goods_advice1,
        goods_advice2,
    ]


@pytest.fixture(params=("advice_view", "countersign_advice_view", "consolidate_advice_view"))
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:{request.param}", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_advice_view_200(mock_queue, mock_case, authorized_client, data_queue, data_standard_case, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_advice_view_heading_no_advice(
    requests_mock, mock_queue, authorized_client, data_queue, data_standard_case, url
):
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "There are no recommendations for this case yet" in soup.find("h2")


def test_advice_view_heading_ogd_advice(
    requests_mock, mock_queue, authorized_client, data_queue, data_standard_case, data_case_advice, url
):
    data_standard_case["case"]["advice"] = data_case_advice
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" in soup.find("h2")
    team_headings = {heading.text.strip() for heading in soup.select("details summary")}
    assert team_headings == {"A team has approved and refused", "B team has approved"}


@mock.patch("caseworker.advice.views.get_gov_user")
def test_fco_cannot_advice_when_all_dests_covered(mock_get_gov_user, authorized_client, data_queue, data_standard_case):
    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    mock_get_gov_user.return_value = (
        {
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM},
            }
        },
        None,
    )
    data_standard_case["case"]["advice"] = [
        # The GB destination has been advised on by FCO
        {
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM},
            },
            "type": {"value": "Approve"},
        },
    ]
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert not response.context_data["can_advise"]
