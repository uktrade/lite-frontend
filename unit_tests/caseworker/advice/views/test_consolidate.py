import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup
from django.urls import reverse

from caseworker.advice import forms
from caseworker.advice import services
from caseworker.advice.services import (
    FCDO_TEAM,
    LICENSING_UNIT_TEAM,
    MOD_CONSOLIDATE_TEAMS,
    MOD_ECJU_TEAM,
    MANPADS_ID,
    AP_LANDMINE_ID,
    LU_COUNTERSIGN_REQUIRED_ID,
    LU_SR_MGR_CHECK_REQUIRED_ID,
)
from core import client
from unit_tests.caseworker.conftest import countersignatures_for_advice


@pytest.fixture
def mock_post_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons, mock_post_team_advice):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def view_consolidate_outcome_url(data_queue, data_standard_case):
    return reverse(
        f"cases:consolidate_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def advice(current_user):
    return [
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "country": None,
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "footnotes",
            "good": good_id,
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",
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


GREEN_COUNTRIES_ID = "64a4933b-555b-49fe-96da-25e0f121050f"
FIREARMS_ID = "00000000-0000-0000-0000-000000000007"
SMALL_ARMS_ID = "318d9c76-f772-4517-bda8-296cdf3191c0"

FLAG_MAP = {
    GREEN_COUNTRIES_ID: {
        "id": GREEN_COUNTRIES_ID,
        "name": "Green Countries",
        "level": "Destination",
        "colour": "green",
        "label": "Green countries",
        "priority": 20,
        "alias": None,
    },
    MANPADS_ID: {
        "id": MANPADS_ID,
        "name": "Manpads",
        "level": "Case",
        "colour": "default",
        "label": "",
        "priority": 0,
        "alias": None,
    },
    AP_LANDMINE_ID: {
        "id": AP_LANDMINE_ID,
        "name": "AP Landmine",
        "level": "Case",
        "colour": "default",
        "label": "",
        "priority": 0,
        "alias": None,
    },
    LU_COUNTERSIGN_REQUIRED_ID: {
        "id": LU_COUNTERSIGN_REQUIRED_ID,
        "name": "LU Countersign Required",
        "level": "Destination",
        "colour": "default",
        "label": "",
        "priority": 0,
        "alias": "LU_COUNTER_REQUIRED",
    },
    LU_SR_MGR_CHECK_REQUIRED_ID: {
        "id": LU_SR_MGR_CHECK_REQUIRED_ID,
        "name": "LU Senior Manager check required",
        "level": "Destination",
        "colour": "default",
        "label": "",
        "priority": 0,
        "alias": "LU_SENIOR_MANAGER_CHECK_REQUIRED",
    },
    FIREARMS_ID: {
        "id": FIREARMS_ID,
        "name": "Firearms",
        "level": "Case",
        "colour": "default",
        "label": None,
        "priority": 0,
        "alias": None,
    },
    SMALL_ARMS_ID: {
        "id": SMALL_ARMS_ID,
        "name": "Small Arms",
        "level": "Good",
        "colour": "default",
        "label": "",
        "priority": 0,
        "alias": None,
    },
}


@pytest.fixture
def advice_to_consolidate(MOD_team1_user, MOD_team2_user, MOD_ECJU_team_user, FCDO_team_user):
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
            "countersign_comments": "Agree with the recommendation",
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
            "text": "Approve from our team",
            "third_party": None,
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": FCDO_team_user,
        },
    ]


@pytest.fixture
def consolidated_advice(current_user, team1_user):
    current_user["team"]["id"] = "2132131d-2432-423424"
    current_user["team"]["alias"] = LICENSING_UNIT_TEAM
    return [
        {
            "id": "4f146dd1-a454-49ad-8c78-214552a45207",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.176613Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "ac914a37-ae50-4a8e-8ebb-0c31b98cfbd2",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.222814Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "deb3e4f7-3704-4dad-aaa5-855a076bb16f",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.262769Z",
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "56a3062a-6437-4e4f-8ce8-87ad76d5d903",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.082345Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "cdf5ac6d-f209-48c9-a6cd-6f7b8496f810",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.123966Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.161135Z",
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "no_licence_required", "value": "No Licence Required"},
            "level": "team",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.161135Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
    ]


@pytest.fixture
def advice_for_lu_countersign(consolidated_advice):
    return [item for item in consolidated_advice if item["level"] == "final"]


def to_refusal_advice(advice):
    for item in advice:
        item["type"] = {"key": "refuse", "value": "Refuse"}
        item["denial_reasons"] = ["5a", "5b"]
    return advice


@pytest.fixture
def refusal_advice(advice):
    return to_refusal_advice(advice)


@pytest.fixture
def consolidated_refusal_outcome(consolidated_advice):
    return to_refusal_advice(consolidated_advice)


@pytest.fixture()
def gov_user():
    return {
        "user": {
            "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "team": {
                "id": "211111b-c111-11e1-1111-1111111111a",
                "name": "Test",
                "alias": "TEST_1",
            },
        }
    }


@pytest.mark.parametrize(
    "path, form_class, team_alias, team_name",
    (
        ("", forms.ConsolidateApprovalForm, LICENSING_UNIT_TEAM, "LU Team"),
        ("", forms.ConsolidateApprovalForm, MOD_ECJU_TEAM, "MOD Team"),
        ("approve/", forms.ConsolidateApprovalForm, LICENSING_UNIT_TEAM, "LU Team"),
        ("refuse/", forms.RefusalAdviceForm, LICENSING_UNIT_TEAM, "LU Team"),
        ("approve/", forms.ConsolidateApprovalForm, MOD_ECJU_TEAM, "MOD Team"),
        ("refuse/", forms.RefusalAdviceForm, MOD_ECJU_TEAM, "MOD Team"),
    ),
)
def test_consolidate_review(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    advice_to_consolidate,
    gov_user,
    path,
    form_class,
    team_alias,
    team_name,
):
    data_standard_case["case"]["advice"] = advice_to_consolidate
    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(url + path)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, form_class)

    advice_to_review = list(response.context["advice_to_consolidate"])
    advice_teams = {item[0]["user"]["team"]["alias"] for item in advice_to_review}

    if team_alias == LICENSING_UNIT_TEAM:
        assert advice_teams == {FCDO_TEAM, MOD_ECJU_TEAM}
    elif team_alias == MOD_ECJU_TEAM:
        assert bool(advice_teams.intersection(MOD_CONSOLIDATE_TEAMS)) == True


@pytest.mark.parametrize(
    "team_alias, team_name, recommendation, redirect",
    [
        (LICENSING_UNIT_TEAM, "Licensing Unit", "approve", "approve"),
        (LICENSING_UNIT_TEAM, "Licensing Unit", "refuse", "refuse"),
        (MOD_ECJU_TEAM, "MOD-ECJU", "approve", "approve"),
        (MOD_ECJU_TEAM, "MOD-ECJU", "refuse", "refuse"),
    ],
)
def test_consolidate_review_refusal_advice(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    refusal_advice,
    gov_user,
    team_alias,
    team_name,
    recommendation,
    redirect,
):
    data_standard_case["case"]["advice"] = refusal_advice
    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.ConsolidateSelectAdviceForm)
    response = authorized_client.post(url, data={"recommendation": recommendation})
    assert response.status_code == 302
    assert redirect in response.url


@pytest.mark.parametrize(
    "team_alias, team_name, recommendation_label",
    [
        (LICENSING_UNIT_TEAM, "Licensing Unit", "What is the combined recommendation for Licensing Unit?"),
        (MOD_ECJU_TEAM, "MOD-ECJU", "What is the combined recommendation for MOD-ECJU?"),
    ],
)
def test_consolidate_review_refusal_advice_recommendation_label(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    refusal_advice,
    team_alias,
    team_name,
    recommendation_label,
    gov_user,
):
    data_standard_case["case"]["advice"] = refusal_advice
    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.ConsolidateSelectAdviceForm)
    assert form.fields["recommendation"].label == recommendation_label


def test_consolidate_review_approve(requests_mock, authorized_client, data_standard_case, url, advice):
    data_standard_case["case"]["advice"] = advice
    data = {"approval_reasons": "test", "countries": ["GB"]}

    response = authorized_client.post(url + "approve/", data=data)
    assert response.status_code == 302
    request = requests_mock.request_history.pop()
    assert request.method == "POST"
    assert "team-advice" in request.url
    assert request.json() == [
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "note": "",
            "proviso": "",
            "text": "test",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "type": "approve",
        },
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "denial_reasons": [],
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


def test_consolidate_review_refuse(requests_mock, authorized_client, data_standard_case, url, advice):
    data_standard_case["case"]["advice"] = advice
    data = {"denial_reasons": ["1"], "refusal_reasons": "test", "countries": ["GB"]}
    response = authorized_client.post(url + "refuse/", data=data)
    assert response.status_code == 302
    request = requests_mock.request_history.pop()
    assert request.method == "POST"
    assert "team-advice" in request.url
    assert request.json() == [
        {
            "denial_reasons": ["1"],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote_required": False,
            "text": "test",
            "type": "refuse",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "type": "refuse",
        },
        {
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "type": "refuse",
        },
        {
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


def test_view_consolidate_approve_outcome(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_advice,
    gov_user,
):
    data_standard_case["case"]["advice"] = consolidated_advice
    gov_user["user"]["team"]["name"] = "Licensing Unit"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == ["Country", "Type", "Name", "Approved products"]

    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "United Kingdom",
        "End-user",
        "End User",
        "All",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
    ]


def test_view_consolidate_refuse_outcome(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_refusal_outcome,
    gov_user,
):
    data_standard_case["case"]["advice"] = consolidated_refusal_outcome
    gov_user["user"]["team"]["name"] = "Licensing Unit"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == [
        "Country",
        "Type",
        "Name",
        "Refused products",
        "Refusal criteria",
    ]

    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "five a, five b",
        "United Kingdom",
        "End-user",
        "End User",
        "All",
        "five a, five b",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
        "five a, five b",
    ]


@pytest.mark.parametrize(
    "path, form_class",
    (
        ("", forms.ConsolidateApprovalForm),
        ("approve/", forms.ConsolidateApprovalForm),
        ("refuse/", forms.RefusalAdviceForm),
    ),
)
def test_consolidate_raises_exception_for_other_team(
    authorized_client, data_standard_case, url, advice, path, form_class
):
    data_standard_case["case"]["advice"] = advice

    with pytest.raises(Exception) as err:
        authorized_client.get(url + path)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


@pytest.mark.parametrize(
    "team_alias, team_name, flag",
    (
        (services.LICENSING_UNIT_TEAM, "LU Team", LU_COUNTERSIGN_REQUIRED_ID),
        (services.LICENSING_UNIT_TEAM, "LU Team", LU_SR_MGR_CHECK_REQUIRED_ID),
        (services.MOD_ECJU_TEAM, "MoD Team", LU_COUNTERSIGN_REQUIRED_ID),
        (services.MOD_ECJU_TEAM, "MoD Team", LU_SR_MGR_CHECK_REQUIRED_ID),
    ),
)
def test_view_consolidate_approve_outcome_countersign_warning_message(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_advice,
    gov_user,
    team_alias,
    team_name,
    flag,
    with_lu_countersigning_disabled,
):
    data_standard_case["case"]["advice"] = consolidated_advice
    flags = [SMALL_ARMS_ID, GREEN_COUNTRIES_ID, FIREARMS_ID, flag]
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in flags]

    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    assert not response.context["rejected_lu_countersignature"]
    if team_alias == services.LICENSING_UNIT_TEAM:
        assert response.context["lu_countersign_required"] is True
        assert response.context["finalise_case"] is False
    else:
        assert response.context["lu_countersign_required"] is False
        assert response.context["finalise_case"] is False


@pytest.mark.parametrize(
    "flags",
    (
        ([LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID]),
        ([LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID]),
        ([MANPADS_ID, GREEN_COUNTRIES_ID]),
        ([AP_LANDMINE_ID, GREEN_COUNTRIES_ID]),
    ),
)
def test_case_returned_info_for_first_countersignature_rejection(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    gov_user,
    flags,
    with_lu_countersigning_enabled,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    # Rejected countersignature
    countersigning_data = [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": False}]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in flags]

    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = services.LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    assert response.context["rejected_lu_countersignature"]
    assert not response.context["rejected_lu_countersignature"]["outcome_accepted"]
    assert response.context["rejected_lu_countersignature"]["reasons"] == "I disagree"

    soup = BeautifulSoup(response.content, "html.parser")
    rejected_div = soup.find(id="rejected-countersignature")
    rejected_detail_div = soup.find(id="rejected-countersignature-detail")
    countersignature_required_div = soup.find(id="countersign-required")
    countersignature_div = soup.find(class_="countersignatures")
    assert rejected_div is not None
    assert rejected_detail_div is not None
    assert countersignature_required_div is None
    assert countersignature_div is None
    warning = rejected_div.find(class_="govuk-warning-text__text").text
    assert "This case has been returned for editing, by countersigner Testy McTest" in warning
    rejected_by = rejected_detail_div.find("h2").text
    assert "Reason for returning" in rejected_by
    assert "I disagree" in rejected_detail_div.find("p").text

    assert not soup.find(id="finalise-case-button")


@pytest.mark.parametrize(
    "flags",
    (
        ([LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID]),
        ([LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID]),
        ([MANPADS_ID, GREEN_COUNTRIES_ID]),
        ([AP_LANDMINE_ID, GREEN_COUNTRIES_ID]),
    ),
)
def test_case_returned_info_for_second_countersignature_rejection(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    gov_user,
    flags,
    with_lu_countersigning_enabled,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    countersigning_data = [
        {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
        {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": False},
    ]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in flags]

    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = services.LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    assert response.context["rejected_lu_countersignature"]
    assert not response.context["rejected_lu_countersignature"]["outcome_accepted"]
    assert response.context["rejected_lu_countersignature"]["reasons"] == "Nope"

    soup = BeautifulSoup(response.content, "html.parser")
    rejected_div = soup.find(id="rejected-countersignature")
    rejected_detail_div = soup.find(id="rejected-countersignature-detail")
    countersignature_required_div = soup.find(id="countersign-required")
    countersignature_div = soup.find(class_="countersignatures")
    assert rejected_div is not None
    assert rejected_detail_div is not None
    assert countersignature_required_div is None
    assert countersignature_div is None
    warning = rejected_div.find(class_="govuk-warning-text__text").text
    assert "This case has been returned for editing, by countersigner Super Visor" in warning
    rejected_by = rejected_detail_div.find("h2").text
    assert "Reason for returning" in rejected_by
    rejected_detail = rejected_detail_div.find("p").text
    assert "Nope" in rejected_detail

    assert not soup.find(id="finalise-case-button")


def test_finalise_button_shown_if_no_rejected_countersignatures(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    gov_user,
    with_lu_countersigning_enabled,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    countersigning_data = [
        {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
        {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": True},
    ]
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[GREEN_COUNTRIES_ID]]

    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = services.LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200
    assert not response.context["rejected_lu_countersignature"]

    soup = BeautifulSoup(response.content, "html.parser")
    rejected_div = soup.find(id="rejected-countersignature")
    countersignature_div = soup.find(class_="countersignatures")
    assert rejected_div is None
    assert countersignature_div is not None
    assert "Senior countersigned by Super Visor" in countersignature_div.find_all("h2")[0].text
    assert "LGTM" in countersignature_div.find_all("p")[0].text
    assert "Countersigned by Testy McTest" in countersignature_div.find_all("h2")[1].text
    assert "I concur" in countersignature_div.find_all("p")[1].text
    assert soup.find(id="finalise-case-button")


@pytest.mark.parametrize(
    ("team_alias", "flags_list", "countersigning_data", "expected_value_finalise_case"),
    [
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID]],
            [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": False}],
            False,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[AP_LANDMINE_ID]],
            [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": False}],
            False,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID]],
            [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True}],
            True,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[AP_LANDMINE_ID]],
            [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True}],
            True,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID], FLAG_MAP[LU_SR_MGR_CHECK_REQUIRED_ID]],
            [
                {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": False},
            ],
            False,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID], FLAG_MAP[MANPADS_ID]],
            [
                {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": False},
            ],
            False,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID], FLAG_MAP[LU_SR_MGR_CHECK_REQUIRED_ID]],
            [
                {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": True},
            ],
            True,
        ),
        (
            services.LICENSING_UNIT_TEAM,
            [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID], FLAG_MAP[MANPADS_ID]],
            [
                {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": True},
            ],
            True,
        ),
        (services.FCDO_TEAM, [FLAG_MAP[GREEN_COUNTRIES_ID]], [], False),
    ],
)
def test_finalise_button_shown_correctly_for_lu_countersigning_scenarios(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    LU_team_user,
    FCDO_team_user,
    with_lu_countersigning_enabled,
    team_alias,
    flags_list,
    countersigning_data,
    expected_value_finalise_case,
):
    """
    Test cases
    1. LM rejects:
      (a) LM flag only
      (b) AP flag only
    2. LM accepts; no SLM check needed
      (a) LM flag only
      (b) AP flag only
    3. LM accepts; SLM rejects
      (a) LM flag and SLM flag
      (b) LM flag and Manpads flag
    4. LM accepts; SLM accepts
      (a) LM flag and SLM flag
      (b) LM flag and Manpads flag
    5. non-LU user e.g. FCDO
    """
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = flags_list

    if team_alias == services.LICENSING_UNIT_TEAM:
        gov_user = {"user": LU_team_user}
    elif team_alias == services.FCDO_TEAM:
        gov_user = {"user": FCDO_team_user}
    else:
        gov_user = None

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert bool(soup.find(id="finalise-case-button")) is expected_value_finalise_case


@pytest.mark.parametrize(
    "countersigning_data",
    (
        [
            {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": False},
        ],
        [
            {"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True},
            {"order": services.SECOND_COUNTERSIGN, "outcome_accepted": False},
        ],
    ),
)
def test_rejection_countersignature_not_displayed_if_feature_flag_off(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    gov_user,
    with_lu_countersigning_disabled,
    countersigning_data,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    # Rejected countersignature
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in [LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID]]

    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = services.LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200
    assert not response.context["rejected_lu_countersignature"]

    soup = BeautifulSoup(response.content, "html.parser")
    rejected_div = soup.find(id="rejected-countersignature")
    countersignature_required_div = soup.find(id="countersign-required")
    assert rejected_div is None
    assert countersignature_required_div is not None
