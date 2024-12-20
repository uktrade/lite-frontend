from unittest import mock

import pytest

from django.urls import reverse

from caseworker.advice import services
from caseworker.advice.constants import AdviceSteps
from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_approval_reason, mock_proviso, mock_footnote_details):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:approve_all_legacy", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_give_approval_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_select_advice_post(authorized_client, requests_mock, data_standard_case, url):
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})

    data = {"approval_reasons": "meets the requirements", "instructions_to_exporter": "no specific instructions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_fco_give_approval_advice_get(mock_get_gov_user, authorized_client, url):
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM}}},
        None,
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert "countries" in response.context_data["form"].fields
    assert response.context_data["form"].fields["countries"].choices == [
        ("GB", "United Kingdom"),
        ("AE-AZ", "Abu Dhabi"),
    ]


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_fco_give_approval_advice_existing_get(mock_get_gov_user, authorized_client, url, data_standard_case):
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM}}},
        None,
    )
    data_standard_case["case"]["advice"] = [
        # The GB destination has been advised on by MOD-DSTL
        {
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "user": {"team": {"id": "809eba0f-f197-4f0f-949b-9af309a844fb", "name": "MOD-DSTL"}},
            "team": {"id": "809eba0f-f197-4f0f-949b-9af309a844fb", "name": "MOD-DSTL"},
        },
        # The AE-AZ destination has been advised on by FCO (should therefore not be rendered)
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "user": {
                "team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM},
            },
            "team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM},
        },
    ]
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert "countries" in response.context_data["form"].fields
    assert response.context_data["form"].fields["countries"].choices == [
        ("GB", "United Kingdom"),
    ]


@pytest.mark.parametrize(
    "countries, approval_reasons, expected_status_code",
    [
        # Valid form
        (["GB"], "test", 302),
        # Valid form with 2 countries
        (["GB", "AE-AZ"], "test", 302),
        # Invalid form - missing countries
        ([], "test", 200),
        # Invalid form - missing approval_reasons
        (["GB"], "", 200),
        # Invalid form - missing countries & approval_reasons
        ([], "", 200),
    ],
)
@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_fcdo_give_approval_advice_post(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    countries,
    approval_reasons,
    expected_status_code,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
):
    mock_get_gov_user.return_value = (
        {"user": {"team": {"id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74", "name": "FCO", "alias": services.FCDO_TEAM}}},
        None,
    )
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})
    data = {"approval_reasons": approval_reasons, "countries": countries}
    response = authorized_client.post(url, data=data)
    assert response.status_code == expected_status_code


@pytest.fixture
def url_desnz(data_queue, data_standard_case):
    return reverse("cases:approve_all", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


@pytest.fixture
def post_to_step(post_to_step_factory, url_desnz):
    return post_to_step_factory(url_desnz)


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_valid(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_advice,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "Data"},
    )
    assert response.status_code == 302


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_valid_add_conditional(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_advice,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )
    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "reason", "add_licence_conditions": True},
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add licence conditions (optional)"

    add_LC_response = post_to_step(
        AdviceSteps.LICENCE_CONDITIONS,
        {"proviso": "proviso"},
    )
    assert add_LC_response.status_code == 200
    soup = beautiful_soup(add_LC_response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add instructions to the exporter, or a reporting footnote (optional)"

    add_instructions_response = post_to_step(
        AdviceSteps.LICENCE_FOOTNOTES,
        {"instructions_to_exporter": "instructions", "footnote_details": "footnotes"},
    )
    assert add_instructions_response.status_code == 302


@pytest.fixture
def mock_proviso_multiple(requests_mock):
    url = client._build_absolute_uri("/picklist/?type=proviso&page=1&disable_pagination=True&show_deactivated=False")
    data = {
        "results": [
            {"name": "condition 1", "text": "condition 1 text"},
            {"name": "condition 2", "text": "condition 2 text"},
            {"name": "condition 3", "text": "condition 3 text"},
        ]
    }
    return requests_mock.get(url=url, json=data)


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_valid_multiple_conditions(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso_multiple,
    mock_footnote_details,
    mock_post_advice,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "reason", "add_licence_conditions": True},
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add licence conditions (optional)"

    add_LC_response = post_to_step(
        AdviceSteps.LICENCE_CONDITIONS,
        {
            "proviso_checkboxes": ["condition_1", "condition_3"],
            "condition_1": "condition 1 abc",
            "condition_3": "condition 3 xyz",
        },
    )
    assert add_LC_response.status_code == 200
    soup = beautiful_soup(add_LC_response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add instructions to the exporter, or a reporting footnote (optional)"

    add_instructions_response = post_to_step(
        AdviceSteps.LICENCE_FOOTNOTES,
        {},
    )
    assert add_instructions_response.status_code == 302
    assert len(mock_post_advice.request_history) == 1
    assert mock_post_advice.request_history[0].json()[0]["proviso"] == "condition 1 abc\n\n--------\ncondition 3 xyz"


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_valid_add_conditional_optional(
    mock_get_gov_user,
    authorized_client,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    mock_post_advice,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": "reason", "add_licence_conditions": True},
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add licence conditions (optional)"

    add_LC_response = post_to_step(
        AdviceSteps.LICENCE_CONDITIONS,
        {},
    )
    assert add_LC_response.status_code == 200
    soup = beautiful_soup(add_LC_response.content)
    # redirected to next form
    header = soup.find("h1")
    assert header.text == "Add instructions to the exporter, or a reporting footnote (optional)"

    add_instructions_response = post_to_step(
        AdviceSteps.LICENCE_FOOTNOTES,
        {},
    )
    assert add_instructions_response.status_code == 302


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_invalid(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.DESNZ_CHEMICAL,
                }
            }
        },
        None,
    )
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})

    response = post_to_step(
        AdviceSteps.RECOMMEND_APPROVAL,
        {"approval_reasons": ""},
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)


@mock.patch("caseworker.advice.views.mixins.get_gov_user")
def test_DESNZ_give_approval_advice_post_invalid_user(
    mock_get_gov_user,
    authorized_client,
    requests_mock,
    data_standard_case,
    url,
    mock_approval_reason,
    mock_proviso,
    mock_footnote_details,
    post_to_step,
    beautiful_soup,
):
    mock_get_gov_user.return_value = (
        {
            "user": {
                "team": {
                    "id": "56273dd4-4634-4ad7-a782-e480f85a85a9",
                    "name": "DESNZ Chemical",
                    "alias": services.FCDO_TEAM,
                }
            }
        },
        None,
    )
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})

    # DESNZ only.
    with pytest.raises(IndexError) as err:
        response = post_to_step(
            AdviceSteps.RECOMMEND_APPROVAL,
            {"approval_reasons": ""},
        )
