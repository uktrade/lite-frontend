import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


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
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    # data_standard_case has no advice
    requests_mock.get(url=case_url, json=data_standard_case)

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "There is no advice for this case yet" in soup.find("h2")


def test_advice_view_heading_ogd_advice(
    requests_mock, mock_queue, authorized_client, data_queue, data_standard_case, data_case_advice, url
):
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=data_standard_case)

    case_data = {**data_standard_case}
    case_data["case"]["advice"] = data_case_advice
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=case_data)

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" in soup.find("h2")

    team_headings = {heading.text.strip() for heading in soup.select("details summary")}
    assert team_headings == {"A team has approved and refused", "B team has approved"}
