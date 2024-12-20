import pytest

from caseworker.advice.services import LICENSING_UNIT_TEAM


def advice_base_fields():
    return {
        "proviso": None,
        "good": None,
        "end_user": None,
        "ultimate_end_user": None,
        "consignee": None,
        "third_party": None,
        "country": None,
        "denial_reasons": [],
        "countersigned_by": None,
        "countersign_comments": "",
        "is_refusal_note": False,
    }


@pytest.fixture
def consolidated_advice(
    current_user,
    team1_user,
    team1,
    LU_team_user,
    lu_team,
):
    current_user["team"]["id"] = "2132131d-2432-423424"
    current_user["team"]["alias"] = LICENSING_UNIT_TEAM
    return [
        {
            **advice_base_fields(),
            "id": "4f146dd1-a454-49ad-8c78-214552a45207",  # /PS-IGNORE
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "footnote": "firearms product for military use",
            "user": team1_user,
            "team": team1,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
        },
        {
            **advice_base_fields(),
            "id": "ac914a37-ae50-4a8e-8ebb-0c31b98cfbd2",  # /PS-IGNORE
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "footnote": "firearms product for military use",
            "user": team1_user,
            "team": team1,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
        },
        {
            **advice_base_fields(),
            "id": "deb3e4f7-3704-4dad-aaa5-855a076bb16f",  # /PS-IGNORE
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "footnote": "firearms product for military use",
            "user": team1_user,
            "team": team1,
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
        },
        {
            **advice_base_fields(),
            "id": "56a3062a-6437-4e4f-8ce8-87ad76d5d903",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "footnote": "",
            "user": LU_team_user,
            "team": lu_team,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
        },
        {
            **advice_base_fields(),
            "id": "cdf5ac6d-f209-48c9-a6cd-6f7b8496f810",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "footnote": "",
            "user": LU_team_user,
            "team": lu_team,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
        },
        {
            **advice_base_fields(),
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",  # /PS-IGNORE
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "footnote": "",
            "user": LU_team_user,
            "team": lu_team,
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
        },
        {
            **advice_base_fields(),
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",  # /PS-IGNORE
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "team",
            "proviso": "no other conditions",
            "footnote": "",
            "user": LU_team_user,
            "team": lu_team,
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
        },
    ]


@pytest.fixture
def advice_for_lu_countersign(consolidated_advice, LU_team_user, lu_team):
    final_advice = [item for item in consolidated_advice if item["level"] == "final"]
    for item in final_advice:
        item["user"] = LU_team_user
        item["team"] = lu_team

    return final_advice
