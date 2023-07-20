import pytest

from unittest.mock import patch

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM, FIRST_COUNTERSIGN, SECOND_COUNTERSIGN
from core import client
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_picklist, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:consolidate_advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@patch("caseworker.advice.views.get_gov_user")
def test_no_advice_summary_for_lu(
    mock_get_gov_user,
    url,
    authorized_client,
    data_queue,
    data_standard_case,
    advice_for_countersign,
):
    data_standard_case["case"]["advice"] = advice_for_countersign
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "21313212-23123-3123-323wq2", "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" in soup.find("h2")


@pytest.mark.parametrize(
    "countersigning_data",
    (
        [
            {"order": FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
        ],
        [
            {"order": SECOND_COUNTERSIGN, "outcome_accepted": True},
            {"order": FIRST_COUNTERSIGN, "outcome_accepted": True},
        ],
    ),
)
@patch("caseworker.advice.views.get_gov_user")
def test_lu_consolidate_check_countersignatures_other_recommendations(
    mock_get_gov_user,
    countersigning_data,
    authorized_client,
    requests_mock,
    data_standard_case,
    advice_for_lu_countersign,
    url,
):
    case_id = data_standard_case["case"]["id"]
    team_id = advice_for_lu_countersign[0]["user"]["team"]["id"]
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign,
        countersigning_data,
    )
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=data_standard_case)
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": team_id, "alias": LICENSING_UNIT_TEAM}}},
        None,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert "Other recommendations for this case" in soup.find("h2")

    all_details = soup.find_all("details", {"class": "govuk-details"})
    assert len(all_details) == 1
    lu_details = all_details[0]
    summary_text = lu_details.find("span", {"class": "govuk-details__summary-text"})
    assert "LU Team has approved" in summary_text.text

    countersign_elements = lu_details.find_all("div", {"class": "countersigned-by"})
    assert len(countersign_elements) == len(countersigning_data)
    for index, element in enumerate(countersign_elements):
        heading = element.find("h2").text
        comment = element.find("p").text
        if countersigning_data[index]["order"] == SECOND_COUNTERSIGN:
            assert heading == "Senior countersigned by Super Visor"
            assert comment == "LGTM"
        if countersigning_data[index]["order"] == FIRST_COUNTERSIGN:
            assert heading == "Countersigned by Testy McTest"
            assert comment == "I concur"
