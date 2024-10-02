import logging
import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from exporter.core.constants import SetPartyFormSteps
from exporter.applications.forms.parties import (
    PartyReuseForm,
    PartySubTypeSelectForm,
    PartyNameForm,
    PartyWebsiteForm,
    PartyAddressForm,
)


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, data_standard_case):
    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def mock_party_create_success(requests_mock, data_standard_case):
    party_id = data_standard_case["case"]["data"]["consignee"]["id"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/')
    yield requests_mock.post(url=url, status_code=201, json={"consignee": {"id": party_id}})


@pytest.fixture
def mock_party_create_fail(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/')
    yield requests_mock.post(url=url, status_code=500, json={})


@pytest.fixture
def add_consignee_url(application_pk):
    return reverse("applications:add_consignee", kwargs={"pk": application_pk})


@pytest.fixture
def set_consignee_url(application_pk):
    return reverse("applications:set_consignee", kwargs={"pk": application_pk})


@pytest.fixture
def post_to_step(post_to_step_factory, set_consignee_url):
    return post_to_step_factory(set_consignee_url)


@pytest.fixture
def application_parties_consignee_summary_url(application_pk):
    return reverse("applications:consignee", kwargs={"pk": application_pk})


@pytest.fixture(autouse=True)
def setup(
    mock_countries,
):
    yield


@pytest.mark.parametrize("reuse_party_response, expected_url", ((True, "consignees_copy"), (False, "set_consignee")))
def test_add_consignee_view(
    application_pk, data_standard_case, add_consignee_url, authorized_client, reuse_party_response, expected_url
):
    response = authorized_client.get(add_consignee_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], PartyReuseForm)

    response = authorized_client.post(
        add_consignee_url,
        data={
            "reuse_party": reuse_party_response,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(f"applications:{expected_url}", kwargs={"pk": application_pk})


def test_set_consignee_end_to_end_post_success(
    set_consignee_url,
    authorized_client,
    post_to_step,
    requests_mock,
    data_standard_case,
    application_pk,
    mock_party_create_success,
):
    response = authorized_client.get(set_consignee_url)

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartySubTypeSelectForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_SUB_TYPE,
        {"sub_type": "government"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartyNameForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_NAME,
        {"name": "test-name"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartyWebsiteForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_WEBSITE,
        {"website": "https://www.example.com"},
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee address"
    assert isinstance(response.context["form"], PartyAddressForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_ADDRESS,
        {"address": "1 somewhere", "country": "US"},
    )

    assert response.status_code == 302

    party_id = data_standard_case["case"]["data"]["consignee"]["id"]

    assert response.url == reverse(
        "applications:consignee_attach_document", kwargs={"pk": application_pk, "obj_pk": party_id}
    )

    consignee_data = requests_mock.request_history.pop().json()
    assert consignee_data == {
        "sub_type": "government",
        "sub_type_other": "",
        "name": "test-name",
        "website": "https://www.example.com",
        "address": "1 somewhere",
        "country": "US",
        "type": "consignee",
    }


def test_set_consignee_end_to_end_post_fail(
    set_consignee_url,
    authorized_client,
    requests_mock,
    data_standard_case,
    application_pk,
    mock_party_create_fail,
    caplog,
    post_to_step,
):
    response = authorized_client.get(set_consignee_url)

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartySubTypeSelectForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_SUB_TYPE,
        {"sub_type": "government"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartyNameForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_NAME,
        {"name": "test-name"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], PartyWebsiteForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_WEBSITE,
        {"website": "https://www.example.com"},
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee address"
    assert isinstance(response.context["form"], PartyAddressForm)

    response = post_to_step(
        SetPartyFormSteps.PARTY_ADDRESS,
        {"address": "1 somewhere", "country": "US"},
    )

    assert response.status_code == 200
    assert len(caplog.records) == 1
    log = caplog.records[0]

    assert log.message == "Error adding consignee to application - response was: 500 - {}"
    assert log.levelno == logging.ERROR


def test_application_parties_consignee_summary(
    authorized_client, application_parties_consignee_summary_url, mock_get_application
):
    response = authorized_client.get(application_parties_consignee_summary_url)
    assertTemplateUsed(response, "applications/consignee.html")
