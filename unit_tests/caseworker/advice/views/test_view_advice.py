import pytest
from uuid import uuid4
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


approve = {"key": "approve", "value": "Approve"}
refuse = {"key": "refuse", "value": "Refuse"}
advice_template = {
    "id": "012345678-0123-0123-0123-0123456789abc",
    "text": "Lorem ipsum.",
    "note": "Consectetur adipisicing elit.",
    "type": None,
    "level": "user",
    "proviso": None,
    "denial_reasons": None,
    "footnote": None,
    "user": None,
    "created_at": "2021-10-13T11:30:15.409500+01:00",
    "good": None,
    "goods_type": None,
    "country": None,
    "end_user": None,
    "ultimate_end_user": None,
    "consignee": None,
    "third_party": None,
}

team1 = {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None}
team2 = {"id": "0017ed1f-390b-4f78-bfca-86300edec300", "name": "team2", "part_of_ecju": None}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": team1,
}

jane_doe = {
    "email": "jane.doe@example.com",
    "first_name": "Jane",
    "id": "11c74ddd-c119-48cc-8696-e096218ca583",
    "last_name": "Doe",
    "role_name": "Super User",
    "status": "Active",
    "team": team2,
}


@pytest.fixture
def data_case_advice(data_standard_case):
    all_advice = []

    end_user_advice1 = {**advice_template}
    end_user_advice1["id"] = str(uuid4())
    end_user_advice1["type"] = approve
    end_user_advice1["user"] = john_smith
    end_user_advice1["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]

    end_user_advice2 = {**advice_template}
    end_user_advice2["id"] = str(uuid4())
    end_user_advice2["type"] = approve
    end_user_advice2["user"] = jane_doe
    end_user_advice2["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]

    consignee_advice1 = {**advice_template}
    consignee_advice1["id"] = str(uuid4())
    consignee_advice1["type"] = approve
    consignee_advice1["user"] = john_smith
    consignee_advice1["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]

    consignee_advice2 = {**advice_template}
    consignee_advice2["id"] = str(uuid4())
    consignee_advice2["type"] = approve
    consignee_advice2["user"] = jane_doe
    consignee_advice2["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]

    third_party_advice1 = {**advice_template}
    third_party_advice1["id"] = str(uuid4())
    third_party_advice1["type"] = approve
    third_party_advice1["user"] = john_smith
    third_party_advice1["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]

    third_party_advice2 = {**advice_template}
    third_party_advice2["id"] = str(uuid4())
    third_party_advice2["type"] = approve
    third_party_advice2["user"] = jane_doe
    third_party_advice2["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]

    all_advice.append(end_user_advice1)
    all_advice.append(end_user_advice2)
    all_advice.append(consignee_advice1)
    all_advice.append(consignee_advice2)
    all_advice.append(third_party_advice1)
    all_advice.append(third_party_advice2)

    return all_advice


def test_advice_view_200(mock_queue, mock_case, authorized_client, data_queue, data_standard_case):
    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_advice_view_heading_no_advice(requests_mock, mock_queue, authorized_client, data_queue, data_standard_case):
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    # data_standard_case has no advice
    requests_mock.get(url=case_url, json=data_standard_case)

    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "There is no advice for this case yet" in soup.find("h2")


def test_advice_view_heading_ogd_advice(
    requests_mock, mock_queue, authorized_client, data_queue, data_standard_case, data_case_advice
):
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=data_standard_case)

    case_data = {**data_standard_case}
    case_data["case"]["advice"] = data_case_advice
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=case_data)

    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" in soup.find("h2")

    team_headings = {heading.text.strip() for heading in soup.select("details summary")}
    assert team_headings == {"team1", "team2"}
