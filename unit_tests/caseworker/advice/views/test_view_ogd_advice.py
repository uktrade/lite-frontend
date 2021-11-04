import pytest
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

team1 = {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "A team", "part_of_ecju": None}
team2 = {"id": "0017ed1f-390b-4f78-bfca-86300edec300", "name": "B team", "part_of_ecju": None}

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
def end_user_advice1(data_standard_case):
    end_user_advice1 = {**advice_template}
    end_user_advice1["id"] = "6cecd825-0582-46e8-b253-4d52a8db3b24"
    end_user_advice1["type"] = approve
    end_user_advice1["user"] = john_smith
    end_user_advice1["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]
    return end_user_advice1


@pytest.fixture
def end_user_advice2(data_standard_case):
    end_user_advice2 = {**advice_template}
    end_user_advice2["id"] = "257c7265-acf8-4bb8-99e3-77142b1b479d"
    end_user_advice2["type"] = approve
    end_user_advice2["user"] = jane_doe
    end_user_advice2["end_user"] = data_standard_case["case"]["data"]["end_user"]["id"]
    return end_user_advice2


@pytest.fixture
def consignee_advice1(data_standard_case):
    consignee_advice1 = {**advice_template}
    consignee_advice1["id"] = "bce1444f-1d56-40e7-8316-ab1d16afd55d"
    consignee_advice1["type"] = approve
    consignee_advice1["user"] = john_smith
    consignee_advice1["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]
    return consignee_advice1


@pytest.fixture
def consignee_advice2(data_standard_case):
    consignee_advice2 = {**advice_template}
    consignee_advice2["id"] = "d0eeacbb-e33e-4889-bb3a-0e314647597f"
    consignee_advice2["type"] = approve
    consignee_advice2["user"] = jane_doe
    consignee_advice2["consignee"] = data_standard_case["case"]["data"]["consignee"]["id"]
    return consignee_advice2


@pytest.fixture
def third_party_advice1(data_standard_case):
    third_party_advice1 = {**advice_template}
    third_party_advice1["id"] = "34365628-d9cf-443f-a34c-362507141be1"
    third_party_advice1["type"] = refuse
    third_party_advice1["user"] = john_smith
    third_party_advice1["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]
    return third_party_advice1


@pytest.fixture
def third_party_advice2(data_standard_case):
    third_party_advice2 = {**advice_template}
    third_party_advice2["id"] = "0ac9eb9a-f9ea-4abd-8c97-9e5113a7ca97"
    third_party_advice2["type"] = approve
    third_party_advice2["user"] = jane_doe
    third_party_advice2["third_party"] = data_standard_case["case"]["data"]["third_parties"][0]["id"]
    return third_party_advice2


@pytest.fixture
def goods_advice1(data_standard_case):
    goods_advice1 = {**advice_template}
    goods_advice1["id"] = "34365628-d9cf-443f-a34c-362507141be1"
    goods_advice1["type"] = refuse
    goods_advice1["user"] = john_smith
    goods_advice1["good"] = data_standard_case["case"]["data"]["goods"][0]["id"]
    return goods_advice1


@pytest.fixture
def goods_advice2(data_standard_case):
    goods_advice2 = {**advice_template}
    goods_advice2["id"] = "0ac9eb9a-f9ea-4abd-8c97-9e5113a7ca97"
    goods_advice2["type"] = approve
    goods_advice2["user"] = jane_doe
    goods_advice2["good"] = data_standard_case["case"]["data"]["goods"][0]["id"]
    return goods_advice2


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
    assert team_headings == {"A team", "B team"}


def test_advice_view_heading_ogd_advice_data(
    requests_mock,
    mock_queue,
    authorized_client,
    data_queue,
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
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=data_standard_case)

    case_data = {**data_standard_case}
    case_data["case"]["advice"] = [
        end_user_advice1,
        end_user_advice2,
        consignee_advice1,
        consignee_advice2,
        third_party_advice1,
        third_party_advice2,
        goods_advice1,
        goods_advice2,
    ]
    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    requests_mock.get(url=case_url, json=case_data)

    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)

    exp_advice = [
        {
            "team": team1,
            "advice": [
                {
                    "user": john_smith,
                    "decision": "Approve",
                    "title": "John Smith has approved",
                    "advice": [
                        {
                            "type": "consignee",
                            "licence_condition": None,
                            "denial_reasons": None,
                            "name": "Consignee",
                            "country": "Abu Dhabi",
                            "advice": consignee_advice1,
                        },
                        {
                            "type": "end_user",
                            "licence_condition": None,
                            "denial_reasons": None,
                            "name": "End User",
                            "country": "United Kingdom",
                            "advice": end_user_advice1,
                        },
                    ],
                },
                {
                    "user": john_smith,
                    "title": "John Smith has refused",
                    "decision": "Refuse",
                    "advice": [
                        {
                            "type": "third_party",
                            "licence_condition": None,
                            "denial_reasons": None,
                            "name": "Third party",
                            "country": "United Kingdom",
                            "advice": third_party_advice1,
                        }
                    ],
                },
            ],
        },
        {
            "team": team2,
            "advice": [
                {
                    "user": jane_doe,
                    "decision": "Approve",
                    "title": "Jane Doe has approved",
                    "advice": [
                        {
                            "type": "consignee",
                            "licence_condition": None,
                            "name": "Consignee",
                            "country": "Abu Dhabi",
                            "denial_reasons": None,
                            "advice": consignee_advice2,
                        },
                        {
                            "type": "end_user",
                            "licence_condition": None,
                            "name": "End User",
                            "country": "United Kingdom",
                            "denial_reasons": None,
                            "advice": end_user_advice2,
                        },
                        {
                            "type": "third_party",
                            "licence_condition": None,
                            "name": "Third party",
                            "country": "United Kingdom",
                            "denial_reasons": None,
                            "advice": third_party_advice2,
                        },
                    ],
                }
            ],
        },
    ]

    assert response.context_data["grouped_advice"] == exp_advice

    # we sort teams by name so these should be alphabetical
    assert response.context_data["grouped_advice"][0]["team"] == team1
    assert response.context_data["grouped_advice"][1]["team"] == team2

    team1_advice = response.context_data["grouped_advice"][0]
    team2_advice = response.context_data["grouped_advice"][1]

    # team1 gave 2 different decisions, team2 only gave 1
    assert len(team1_advice["advice"]) == 2
    assert len(team2_advice["advice"]) == 1

    # team1 approved 2 destinations
    assert team1_advice["advice"][0]["decision"] == "Approve"
    assert len(team1_advice["advice"][0]["advice"]) == 2
    assert team1_advice["advice"][0]["advice"][0]["type"] == "consignee"
    assert team1_advice["advice"][0]["advice"][1]["type"] == "end_user"

    # team1 refused 1 destination
    assert team1_advice["advice"][1]["decision"] == "Refuse"
    assert len(team1_advice["advice"][1]["advice"]) == 1
    assert team1_advice["advice"][1]["advice"][0]["type"] == "third_party"

    # team2 approved all three destinations
    assert team2_advice["advice"][0]["decision"] == "Approve"
    assert len(team2_advice["advice"][0]["advice"]) == 3
    assert team2_advice["advice"][0]["advice"][0]["type"] == "consignee"
    assert team2_advice["advice"][0]["advice"][1]["type"] == "end_user"
    assert team2_advice["advice"][0]["advice"][2]["type"] == "third_party"
