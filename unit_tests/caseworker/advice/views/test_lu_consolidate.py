import pytest

from unittest.mock import patch

from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice.services import LICENSING_UNIT_TEAM, FIRST_COUNTERSIGN, SECOND_COUNTERSIGN
from core import client
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_approval_reason, mock_proviso, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:consolidate_advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@patch("caseworker.advice.views.mixins.get_gov_user")
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
@patch("caseworker.advice.views.mixins.get_gov_user")
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


@pytest.fixture
def advice(current_user):
    return [
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",  # /PS-IGNORE
            "country": None,
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "footnotes",
            "good": good_id,
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "level": "user",
            "note": "additional notes",
            "proviso": "no conditions",
            "text": "meets the criteria",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": current_user,
        }
        for good_id in ("0bedd1c3-cf97-4aad-b711-d5c9a9f4586e", "6daad1c3-cf97-4aad-b711-d5c9a9f4586e")
    ]


@pytest.fixture
def url_consolidate_review(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@patch("caseworker.advice.views.mixins.get_gov_user")
def test_refusal_note_post(
    mock_get_gov_user, requests_mock, authorized_client, data_standard_case, url_consolidate_review
):
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "21313212-23123-3123-323wq2", "alias": LICENSING_UNIT_TEAM}}},
        None,
    )

    requests_mock.post(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice/"), json={})

    response = authorized_client.post(
        url_consolidate_review + "refuse/", data={"denial_reasons": ["1a"], "refusal_note": "test"}
    )
    assert response.status_code == 302
    request = requests_mock.request_history.pop()
    assert "final-advice" in request.url
    assert request.json() == [
        {
            "type": "refuse",
            "text": "test",
            "footnote_required": False,
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "denial_reasons": ["1a"],
            "is_refusal_note": True,
        },
        {
            "type": "refuse",
            "text": "test",
            "footnote_required": False,
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1a"],
            "is_refusal_note": True,
        },
        {
            "type": "refuse",
            "text": "test",
            "footnote_required": False,
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "denial_reasons": ["1a"],
            "is_refusal_note": True,
        },
        {
            "type": "refuse",
            "text": "test",
            "footnote_required": False,
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "denial_reasons": ["1a"],
            "is_refusal_note": True,
        },
        {
            "type": "no_licence_required",
            "text": "",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "denial_reasons": [],
        },
        {
            "type": "no_licence_required",
            "text": "",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "denial_reasons": [],
        },
    ]
