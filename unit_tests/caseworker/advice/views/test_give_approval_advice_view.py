from unittest import mock

import pytest

from django.urls import reverse

from caseworker.advice import services


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_approval_reason, mock_proviso, mock_footnote_details):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse("cases:approve_all", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})


def test_give_approval_advice_get(authorized_client, url):
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_select_advice_post(authorized_client, requests_mock, data_standard_case, url):
    requests_mock.post(f"/cases/{data_standard_case['case']['id']}/user-advice/", json={})

    data = {"approval_reasons": "meets the requirements", "instructions_to_exporter": "no specific instructions"}
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302


@mock.patch("caseworker.advice.views.get_gov_user")
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


@mock.patch("caseworker.advice.views.get_gov_user")
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
@mock.patch("caseworker.advice.views.get_gov_user")
def test_fco_give_approval_advice_post(
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
