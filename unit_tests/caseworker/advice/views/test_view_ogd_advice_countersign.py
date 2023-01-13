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
def group_advice(MOD_team1_user, MOD_team2_user, MOD_ECJU_team_user, FCDO_team_user):
    return [
        {
            "consignee": None,
            "countersign_comments": "",
            "countersigned_by": None,
            "created_at": "2022-01-05T11:18:57.172872Z",
            "denial_reasons": [],
            "end_user": "76de33f4-7834-4eb7-871a-66be3270fb59",
            "footnote": "",
            "good": None,
            "goods_type": None,
            "id": "ee47632b-5dd0-474b-a95d-86e975a95503",
            "level": "user",
            "note": "",
            "proviso": "licence condition ABC",
            "text": "approve no issues",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_team1_user,
        },
        {
            "consignee": None,
            "countersign_comments": "",
            "countersigned_by": None,
            "country": None,
            "created_at": "2022-01-05T11:23:35.473052Z",
            "denial_reasons": [],
            "end_user": "76de33f4-7834-4eb7-871a-66be3270fb59",
            "footnote": "Here is a reporting footnote",
            "good": None,
            "goods_type": None,
            "id": "ebd57168-562f-455d-aa89-59e2f5df0367",
            "level": "user",
            "note": "Here is an exporter instruction",
            "proviso": "No other licence conditions",
            "text": "Approve from our team",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_team2_user,
        },
        {
            "consignee": None,
            "countersign_comments": "",
            "countersigned_by": None,
            "country": None,
            "created_at": "2022-01-05T11:20:52.959163Z",
            "denial_reasons": [],
            "end_user": "76de33f4-7834-4eb7-871a-66be3270fb59",
            "footnote": "",
            "good": None,
            "goods_type": None,
            "id": "de9c95ad-b2e4-46fa-968f-1f2daf289327",
            "level": "team",
            "note": "",
            "proviso": "Meets the criteria",
            "text": "Meets the criteria for issuing the licence",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_ECJU_team_user,
        },
        {
            "consignee": None,
            "countersign_comments": "agree recommendation to refuse. Head of Cases in ECJU-FCDO agreed the recommendation to refuse\r\nNartin Mario - ECJU - FCDO",
            "countersigned_by": {
                "email": "countersigner@example.com",
                "first_name": "Countersigner",
                "id": "fad1db47-c5e1-4788-af3d-aea87523826b",
                "last_name": "Team",
                "role_name": "Super User",
                "status": "Active",
                "team": {
                    "id": "809eba0f-f197-4f0f-949b-9af309a844fb",
                    "is_ogd": True,
                    "name": "FCO",
                    "part_of_ecju": True,
                },
            },
            "country": None,
            "created_at": "2022-01-05T11:25:11.545878Z",
            "denial_reasons": [],
            "end_user": "76de33f4-7834-4eb7-871a-66be3270fb59",
            "footnote": "",
            "good": None,
            "goods_type": None,
            "id": "217e7264-7f28-46ff-bf01-dc64f4432786",
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "On behalf of the ECJU-FCDO Desk Officer for Buckinghamshire, their recommendation to refuse is as follows:\r\n\r\nThis licence would permit the export of miniature broccoli and associated accessories for stock. Ultimate end users are unknown.\r\n\r\nBased on the information available, alongside the unacceptable risk of diversion, I recommend to DIT that they refuse this licence.\r\n\r\nSarah Alcatraz ECJU-FCDO",
            "third_party": None,
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": FCDO_team_user,
        },
    ]


# test for presence of countersign comment (e.g. FCDO countersign)
def test_show_countersign_comment_for_countersigning_team(
    authorized_client, data_standard_case, group_advice, data_queue
):
    data_standard_case["case"]["advice"] = group_advice
    # set up advice list in the case

    # something else
    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)

    # use soup to check page for text
    soup = BeautifulSoup(response.content, "html.parser")

    assert "Countersigned by Countersigner Team" in [h2.text for h2 in soup.find_all("h2")]
    assert (
        "agree recommendation to refuse. Head of Cases in ECJU-FCDO agreed the recommendation to refuse\r\nNartin Mario - ECJU - FCDO"
        in [p.text for p in soup.find_all("p")]
    )


# test that countersign comment does not show (e.g. MOD doesn't countersign)
def test_do_not_show_countersign_comment_for_non_countersigning_team():
    pass
