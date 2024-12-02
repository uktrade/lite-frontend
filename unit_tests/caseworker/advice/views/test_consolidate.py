import pytest
import uuid
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


@pytest.fixture
def mock_get_ecju_open_count(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries-open-count/")
    yield requests_mock.get(url=url, json={"count": 0})


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_proviso,
    mock_footnote_details,
    mock_post_team_advice,
    mock_finalise_advice_documents,
    mock_get_ecju_open_count,
):
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
def advice(current_user, admin_team):
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
            "team": admin_team,
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
def advice_to_consolidate(
    MOD_team1_user,
    MOD_team1,
    MOD_team2_user,
    MOD_team2,
    MOD_ECJU_team_user,
    MOD_ECJU_team,
    FCDO_team_user,
    fcdo_team,
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
            "team": MOD_ECJU_team,
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
            "team": fcdo_team,
        },
    ]


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
        ("approve/", forms.ConsolidateApprovalForm, LICENSING_UNIT_TEAM, "LU Team"),
        ("refuse/", forms.LUConsolidateRefusalForm, LICENSING_UNIT_TEAM, "LU Team"),
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


def test_approval_reasons_mocked(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    advice_to_consolidate,
    gov_user,
):
    data_standard_case["case"]["advice"] = advice_to_consolidate
    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(url + "approve/")
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.GiveApprovalAdviceForm)
    # this is built mock_approval_reason
    response_choices = [list(choice) for choice in form.fields["approval_radios"].choices]
    assert response_choices == [
        ["no_concerns", "no concerns"],
        ["concerns", "concerns"],
        ["wmd", "wmd"],
        ["other", "Other"],
    ]
    assert form.approval_text == {
        "no_concerns": "No Concerns Text",
        "concerns": "Concerns Text",
        "wmd": "Weapons of mass destruction Text",
        "other": "",
    }


def test_approval_reasons_manual(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    advice_to_consolidate,
    gov_user,
):
    data_standard_case["case"]["advice"] = advice_to_consolidate
    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    requests_mock.get(
        client._build_absolute_uri(
            "/picklist/?type=standard_advice&page=1&disable_pagination=True&show_deactivated=False"
        ),
        json={
            "results": [
                {"name": "custom Value", "text": "This Casing is Maintained"},
                {"name": "another custom value with many spaces", "text": "Concerns Text"},
                {"name": "ALLCAPSNOSPACES", "text": "This is all caps text"},
            ]
        },
    )
    response = authorized_client.get(url + "approve/")
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.GiveApprovalAdviceForm)
    response_choices = [list(choice) for choice in form.fields["approval_radios"].choices]

    assert list(response_choices) == [
        ["custom_value", "custom Value"],
        ["another_custom_value_with_many_spaces", "another custom value with many spaces"],
        ["allcapsnospaces", "ALLCAPSNOSPACES"],
        ["other", "Other"],
    ]
    assert form.approval_text == {
        "custom_value": "This Casing is Maintained",
        "another_custom_value_with_many_spaces": "Concerns Text",
        "allcapsnospaces": "This is all caps text",
        "other": "",
    }


def test_proviso_manual(
    requests_mock,
    authorized_client,
    data_standard_case,
    url,
    advice_to_consolidate,
    gov_user,
):
    data_standard_case["case"]["advice"] = advice_to_consolidate
    gov_user["user"]["team"]["name"] = "LU Team"
    gov_user["user"]["team"]["alias"] = LICENSING_UNIT_TEAM

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    requests_mock.get(
        client._build_absolute_uri("/picklist/?type=proviso&page=1&disable_pagination=True&show_deactivated=False"),
        json={
            "results": [
                {"name": "custom Value", "text": "This Casing is Maintained"},
                {"name": "another custom value with many spaces", "text": "Concerns Text"},
                {"name": "ALLCAPSNOSPACES", "text": "This is all caps text"},
            ]
        },
    )
    response = authorized_client.get(url + "approve/")
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.GiveApprovalAdviceForm)
    response_choices = [list(choice) for choice in form.fields["proviso_radios"].choices]

    assert list(response_choices) == [
        ["custom_value", "custom Value"],
        ["another_custom_value_with_many_spaces", "another custom value with many spaces"],
        ["allcapsnospaces", "ALLCAPSNOSPACES"],
        ["other", "Other"],
    ]
    assert form.proviso_text == {
        "custom_value": "This Casing is Maintained",
        "another_custom_value_with_many_spaces": "Concerns Text",
        "allcapsnospaces": "This is all caps text",
        "other": "",
    }


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
            "is_refusal_note": False,
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "ultimate_end_user": "9f077b3c-6116-4111-b9a0-b2491198aa72",
            "type": "refuse",
            "is_refusal_note": False,
        },
        {
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
            "is_refusal_note": False,
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
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_advice,
    mock_gov_lu_user,
):
    data_standard_case["case"]["advice"] = consolidated_advice

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
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_refusal_outcome,
    mock_gov_lu_user,
):
    data_standard_case["case"]["advice"] = consolidated_refusal_outcome

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
    "flags, countersigning_data",
    (
        (
            [LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": False}],
        ),
        (
            [LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": False}],
        ),
        (
            [MANPADS_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": False}],
        ),
        (
            [AP_LANDMINE_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": False}],
        ),
        # Countersignatures become invalid when caseworker edits their recommendation following rejection
        (
            [LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": False}],
        ),
        (
            [LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": False}],
        ),
        (
            [MANPADS_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": False}],
        ),
        (
            [AP_LANDMINE_ID, GREEN_COUNTRIES_ID],
            [{"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": False}],
        ),
    ),
)
def test_case_returned_info_for_first_countersignature_rejection(
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    mock_gov_lu_user,
    flags,
    countersigning_data,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    # Rejected countersignature
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in flags]

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    # When caseworker edits recommendation all previous countersignatures are
    # marked as invalid hence there will only be one set of valid countersignatures
    countersignature_valid = any(item["valid"] for item in countersigning_data)

    if countersignature_valid:
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
    else:
        assert response.context["rejected_lu_countersignature"] is None
        soup = BeautifulSoup(response.content, "html.parser")
        countersign_required_div = soup.find(id="countersign-required")
        warning = countersign_required_div.find(class_="govuk-warning-text__text").text
        assert (
            "This case requires countersigning. Moving this case on will pass it to the countersigning work queue."
            in warning
        )
        assert not soup.find(id="finalise-case-button")


@pytest.mark.parametrize(
    "flags, countersigning_data",
    (
        (
            [LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": True, "outcome_accepted": False},
            ],
        ),
        (
            [LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": True, "outcome_accepted": False},
            ],
        ),
        (
            [MANPADS_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": True, "outcome_accepted": False},
            ],
        ),
        (
            [AP_LANDMINE_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": True, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": True, "outcome_accepted": False},
            ],
        ),
        # Countersignatures become invalid when caseworker edits their recommendation following rejection
        (
            [LU_COUNTERSIGN_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": False, "outcome_accepted": False},
            ],
        ),
        (
            [LU_SR_MGR_CHECK_REQUIRED_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": False, "outcome_accepted": False},
            ],
        ),
        (
            [MANPADS_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": False, "outcome_accepted": False},
            ],
        ),
        (
            [AP_LANDMINE_ID, GREEN_COUNTRIES_ID],
            [
                {"order": services.FIRST_COUNTERSIGN, "valid": False, "outcome_accepted": True},
                {"order": services.SECOND_COUNTERSIGN, "valid": False, "outcome_accepted": False},
            ],
        ),
    ),
)
def test_case_returned_info_for_second_countersignature_rejection(
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    mock_gov_lu_user,
    flags,
    countersigning_data,
):
    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, countersigning_data
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[k] for k in flags]

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    # When caseworker edits recommendation all previous countersignatures are
    # marked as invalid hence there will only be one set of valid countersignatures
    countersignature_valid = any(item["valid"] for item in countersigning_data)

    if countersignature_valid:
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
    else:
        assert response.context["rejected_lu_countersignature"] is None
        soup = BeautifulSoup(response.content, "html.parser")
        countersign_required_div = soup.find(id="countersign-required")
        warning = countersign_required_div.find(class_="govuk-warning-text__text").text
        assert (
            "This case requires countersigning. Moving this case on will pass it to the countersigning work queue."
            in warning
        )
        assert not soup.find(id="finalise-case-button")


def test_finalise_button_shown_if_no_rejected_countersignatures(
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    mock_gov_lu_user,
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
    "open_queries_count, expected_value_finalise_case, open_query_warning_displayed",
    [
        [0, True, False],
        [1, False, True],
    ],
)
def test_finalise_has_open_queries_warning_displayed_correctly(
    requests_mock,
    authorized_client,
    data_standard_case,
    standard_case_pk,
    view_consolidate_outcome_url,
    advice_for_lu_countersign,
    LU_team_user,
    open_queries_count,
    expected_value_finalise_case,
    open_query_warning_displayed,
):
    """
    Test cases
    1. finialise button is available because we don't have any open queries
    1. finialise button isn't available warning is displayed because we have open queries
    """

    data_standard_case["case"]["advice"] = advice_for_lu_countersign
    data_standard_case["case"]["countersign_advice"] = countersignatures_for_advice(
        advice_for_lu_countersign, [{"order": services.FIRST_COUNTERSIGN, "outcome_accepted": True}]
    )
    data_standard_case["case"]["all_flags"] = [FLAG_MAP[LU_COUNTERSIGN_REQUIRED_ID]]

    gov_user = {"user": LU_team_user}

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries-open-count/"),
        json={"count": open_queries_count},
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert bool(soup.find(id="finalise-case-button")) is expected_value_finalise_case
    assert bool(soup.find(id="case-has-open-queries")) is open_query_warning_displayed


@pytest.mark.parametrize(
    "decision_document",
    [
        {"documents": {"inform": {"value": "Inform"}}},
        {"documents": {"refuse": {"value": "Refuse"}, "inform": {"value": "Inform"}}},
    ],
)
def test_decision_document_present(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_refusal_outcome,
    mock_gov_lu_user,
    decision_document,
    settings,
):
    data_standard_case["case"]["advice"] = consolidated_refusal_outcome

    decision_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice-documents/")
    requests_mock.get(url=decision_url, json=decision_document)

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    assert response.context["decisions"] == {"inform": {"value": "Inform"}}

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", attrs={"name": "decision_document"})
    assert bool(table) is True


@pytest.mark.parametrize(
    "visible_to_exporter, expected_status",
    [
        [False, "READY TO SEND"],
        [True, "SENT"],
    ],
)
def test_decision_document_status(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_refusal_outcome,
    mock_gov_lu_user,
    visible_to_exporter,
    expected_status,
    settings,
):

    data_standard_case["case"]["advice"] = consolidated_refusal_outcome

    decision_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice-documents/")
    response_json = {
        "documents": {
            "refuse": {"value": "Refuse"},
            "inform": {
                "value": "Inform",
                "document": {"id": str(uuid.uuid4()), "visible_to_exporter": visible_to_exporter},
            },
        }
    }
    requests_mock.get(url=decision_url, json=response_json)

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", attrs={"name": "decision_document"})
    assert table.find("div", {"id": "status-inform"}).text == expected_status


def test_decision_document_not_present(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_advice,
    mock_gov_lu_user,
    settings,
):

    data_standard_case["case"]["advice"] = consolidated_advice

    decision_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/final-advice-documents/")
    requests_mock.get(url=decision_url, json={})

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    assert response.context["decisions"] == {}

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", attrs={"name": "decision_document"})
    assert bool(table) is False


def test_decision_document_recreate_url(
    requests_mock,
    authorized_client,
    data_standard_case,
    data_queue,
    view_consolidate_outcome_url,
    consolidated_refusal_outcome,
    mock_gov_lu_user,
    settings,
):

    case_id = data_standard_case["case"]["id"]
    data_standard_case["case"]["advice"] = consolidated_refusal_outcome

    decision_url = client._build_absolute_uri(f"/cases/{case_id}/final-advice-documents/")
    create_inform_letter_url = f"/queues/{data_queue['id']}/cases/{case_id}/letters/select-inform-template/"

    response_json = {
        "documents": {
            "refuse": {"value": "Refuse", "document": {"id": str(uuid.uuid4()), "visible_to_exporter": True}},
            "inform": {
                "value": "Inform",
                "document": {"id": str(uuid.uuid4()), "visible_to_exporter": True},
            },
        }
    }

    requests_mock.get(url=decision_url, json=response_json)

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="generate-document-inform").attrs["href"] == create_inform_letter_url
