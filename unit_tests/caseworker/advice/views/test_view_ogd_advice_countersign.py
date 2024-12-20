import pytest
from bs4 import BeautifulSoup
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_denial_reasons, mock_approval_reason, mock_proviso, mock_case):
    yield


@pytest.fixture
def group_advice(
    MOD_team1_user,
    MOD_team1,
    MOD_team2_user,
    MOD_team2,
    MOD_ECJU_team_user,
    MOD_ECJU_team,
    FCDO_team_user,
    fcdo_team,
    LU_team_user,
    lu_team,
):
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
            "id": "ee47632b-5dd0-474b-a95d-86e975a95503",
            "level": "user",
            "note": "",
            "proviso": "licence condition ABC",
            "text": "approve no issues",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_team1_user,
            "team": MOD_team1,
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
            "id": "ebd57168-562f-455d-aa89-59e2f5df0367",
            "level": "user",
            "note": "Here is an exporter instruction",
            "proviso": "No other licence conditions",
            "text": "Approve from our team",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_team2_user,
            "team": MOD_team2,
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
            "id": "de9c95ad-b2e4-46fa-968f-1f2daf289327",
            "level": "team",
            "note": "",
            "proviso": "Meets the criteria",
            "text": "Meets the criteria for issuing the licence",
            "third_party": None,
            "type": {"key": "proviso", "value": "Proviso"},
            "ultimate_end_user": None,
            "user": MOD_ECJU_team_user,
            "team": MOD_ECJU_team,
        },
        {
            "consignee": None,
            "countersign_comments": "Agree recommendation to refuse. Person Name - FCDO Countersigning Office",
            "countersigned_by": {
                "email": "countersigner@example.com",
                "first_name": "FCDO Countersigner",
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
            "id": "217e7264-7f28-46ff-bf01-dc64f4432786",
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "I recommend that this license be refused.",
            "third_party": None,
            "type": {"key": "refuse", "value": "Refuse"},
            "ultimate_end_user": None,
            "user": FCDO_team_user,
            "team": fcdo_team,
        },
        {
            "consignee": None,
            "countersign_comments": "Agree recommendation to refuse. Person Name - LU Countersigning Office",
            "countersigned_by": {
                "email": "countersigner@example.com",
                "first_name": "LU Countersigner",
                "id": "fad1db47-c5e1-4788-af3d-aea87523826b",
                "last_name": "Team",
                "role_name": "Super User",
                "status": "Active",
                "team": {
                    "id": "809eba0f-f197-4f0f-949b-9af309a844fb",
                    "is_ogd": True,
                    "name": "LICENSING_UNIT",
                    "part_of_ecju": False,
                },
            },
            "country": None,
            "created_at": "2022-01-05T11:25:11.545878Z",
            "denial_reasons": [],
            "end_user": "76de33f4-7834-4eb7-871a-66be3270fb59",
            "footnote": "",
            "good": None,
            "id": "217e7264-7f28-46ff-bf01-dc64f4432786",
            "level": "user",
            "note": "",
            "proviso": None,
            "text": "I recommend that this license be refused.",
            "third_party": None,
            "type": {"key": "refuse", "value": "Refuse"},
            "ultimate_end_user": None,
            "user": LU_team_user,
            "team": lu_team,
        },
    ]


def test_show_countersign_comment_for_countersigning_team(
    authorized_client, data_standard_case, group_advice, data_queue
):
    data_standard_case["case"]["advice"] = group_advice

    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    list_of_details = soup.find_all("details", class_="govuk-details")

    # Find details tag for specific team by label
    fcdo_team_details = [d for d in list_of_details if "FCDO Team has refused" in str(d)]
    # Check countersign heading
    assert "Countersigned by FCDO Countersigner Team" in "".join(str(fcdo_team_details))
    # Check user details that countersigned
    assert "Refused by FCDO Team User" in "".join(str(fcdo_team_details))
    # Check countersign comments
    assert "Agree recommendation to refuse. Person Name - FCDO Countersigning Office" in "".join(str(fcdo_team_details))

    # Find details tag for specific team by label
    lu_team_details = [d for d in list_of_details if "LU Team has refused" in str(d)]
    # Check countersign heading
    assert "Countersigned by LU Countersigner Team" in "".join(str(lu_team_details))
    # Check user details that countersigned
    assert "Refused by LU Team User" in "".join(str(lu_team_details))
    # Check countersign comments
    assert "Agree recommendation to refuse. Person Name - LU Countersigning Office" in "".join(str(lu_team_details))


def test_do_not_show_countersign_comment_for_non_countersigning_team(
    authorized_client, data_standard_case, group_advice, data_queue
):
    data_standard_case["case"]["advice"] = group_advice

    url = reverse("cases:advice_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # There are exactly two countersigning teams in the test data
    assert ["Countersigned by" in h2.text for h2 in soup.find_all("h2")].count(True) == 2

    list_of_details = soup.find_all("details", class_="govuk-details")

    # Find details tag for specific team by label
    mod_team1_details = [d for d in list_of_details if "Approved by MoD Team1 User" in str(d)]
    # Check for absence of countersign comment
    assert "Countersigned by" not in str(mod_team1_details)

    # Find details tag for specific team by label
    mod_team2_details = [d for d in list_of_details if "Approved by MoD Team2 User" in str(d)]
    # Check for absence of countersign comment
    assert "Countersigned by" not in str(mod_team2_details)

    # Find details tag for specific team by label
    mod_ecju_team_details = [d for d in list_of_details if "Approved by MoD ECJU User" in str(d)]
    # Check for absence of countersign comment
    assert "Countersigned by" not in str(mod_ecju_team_details)
