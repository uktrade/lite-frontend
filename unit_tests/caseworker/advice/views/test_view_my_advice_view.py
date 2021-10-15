import pytest

from bs4 import BeautifulSoup
from copy import deepcopy
from django.urls import reverse

from core import client


@pytest.fixture
def standard_case_with_advice():
    return {
        "id": "2c14d003-1234-4c11-a0fd-bbfd7572c5a4",
        "data": {
            "goods": [
                {
                    "application": "2c14d003-bdbe-4c11-a0fd-bbfd7572c5a4",
                    "control_list_entries": [
                        {
                            "id": "9622ee4e-3f3a-4f3d-ac5f-08280c9e81c9",
                            "rating": "ML6b1",
                            "text": "clc entry description",
                        }
                    ],
                    "created_at": "2021-09-28T16:01:14.707454+01:00",
                    "good": {
                        "comment": None,
                        "control_list_entries": [
                            {
                                "id": "9622ee4e-3f3a-4f3d-ac5f-08280c9e81c9",
                                "rating": "ML6b1",
                                "text": "clc entry description",
                            }
                        ],
                        "description": "Pair of shotgun barrels",
                        "is_good_controlled": {"key": "True", "value": "Yes"},
                        "name": "Pair of shotgun barrels",
                    },
                    "id": "9fbffa7f-ef50-402e-93ac-2f3f37d09030",
                    "is_good_controlled": {"key": "True", "value": "Yes"},
                    "is_good_incorporated": True,
                    "quantity": 2.0,
                    "report_summary": "firearms",
                    "unit": {"key": "NAR", "value": "Number of articles"},
                    "value": "13800.00",
                },
                {
                    "application": "2c14d003-bdbe-4c11-a0fd-bbfd7572c5a4",
                    "control_list_entries": [],
                    "created_at": "2021-09-28T16:03:09.172821+01:00",
                    "good": {
                        "comment": None,
                        "control_list_entries": [],
                        "description": "Pair of shotgun barrels",
                        "is_good_controlled": {"key": "True", "value": "Yes"},
                        "name": "Pair of shotgun barrels 12 bore",
                        "report_summary": None,
                    },
                    "id": "d4feac1e-851d-41a5-b833-eb28addb8547",
                    "is_good_controlled": {"key": "False", "value": "No"},
                    "report_summary": "firearms",
                    "unit": {"key": "NAR", "value": "Number of articles"},
                    "value": "6900.00",
                },
            ]
        },
        "advice": [
            {
                "consignee": None,
                "country": None,
                "created_at": "2021-10-16T23:48:39.486679+01:00",
                "denial_reasons": [],
                "end_user": None,
                "footnote": "footnotes",
                "good": "73152304-6026-4cc0-a3d7-0a93048ecdce",
                "id": "429c5596-fe8b-4540-988b-c37805cd08de",
                "level": "user",
                "note": "additional notes",
                "proviso": "no conditions",
                "text": "meets the criteria",
                "third_party": None,
                "type": {"key": "proviso", "value": "Proviso"},
                "ultimate_end_user": None,
                "user": {
                    "email": "test.user@example.com",
                    "first_name": "Test",
                    "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                    "last_name": "User",
                    "role_name": "Super User",
                    "status": "Active",
                    "team": {
                        "id": "00000000-1234-0000-0000-e676b794b394",
                        "is_ogd": False,
                        "name": "Admin",
                        "part_of_ecju": None,
                    },
                },
            }
        ],
    }


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:view_my_advice", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_view_my_advice_with_conditions_notes_and_nlr_products(
    authorized_client, requests_mock, data_standard_case, standard_case_with_advice, url
):
    """
    Tests display of the 'Approve all' advice given by the user with some conditions attached (proviso)
    and notes to the exporter. One of the product in this application is NLR so it also check
    if NLR products are listed on the page
    """
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = standard_case_with_advice["advice"]

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{data_standard_case['case']['id']}"),
        json={"user": {"id": "58e62718-e889-4a01-b603-e676b794b394"}},
    )

    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table_rows = soup.find("table", id="table-licenceable-products").find_all("tr")
    assert len(table_rows) == 3  # including header

    # Assert on Parties
    expected_headers = ["Country", "Type", "Name", "Approved products"]
    consignee = case_data["case"]["data"]["consignee"]
    expected_consignee_values = [consignee["country"]["name"], "Consignee", consignee["name"], "All"]
    end_user = case_data["case"]["data"]["end_user"]
    expected_end_user_values = [end_user["country"]["name"], "End user", end_user["name"], "All"]

    assert expected_headers == [column.text for column in table_rows[0].find_all("th")]
    assert expected_consignee_values == [column.text for column in table_rows[1].find_all("td")]
    assert expected_end_user_values == [column.text for column in table_rows[2].find_all("td")]

    # Assert Advice
    advice_content = [
        p.text for item in soup.findAll("div", {"class": "govuk-cookie-banner__content"}) for p in item.findAll("p")
    ]
    assert len(advice_content) == 3
    assert advice_content[0] == case_data["case"]["advice"][0]["text"]
    assert advice_content[1] == case_data["case"]["advice"][0]["proviso"]
    assert advice_content[2] == case_data["case"]["advice"][0]["note"]

    # Assert NLR - the second product on this application is NLR
    nlr_table_rows = soup.find("table", id="table-nlr-products").find_all("tr")
    assert ["Product name"] == [column.text for column in nlr_table_rows[0].find_all("th")]
    assert [case_data["case"]["data"]["goods"][1]["good"]["name"]] == [
        column.text for column in nlr_table_rows[1].find_all("td")
    ]
