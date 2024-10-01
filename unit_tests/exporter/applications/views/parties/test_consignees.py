import pytest
from bs4 import BeautifulSoup

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client
from exporter.core.constants import SetPartyFormSteps


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, data_standard_case):
    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def mock_party_create(requests_mock, data_standard_case):
    party_id = data_standard_case["case"]["data"]["consignee"]["id"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/')
    yield requests_mock.post(url=url, status_code=201, json={"consignee": {"id": party_id}})


@pytest.fixture
def mock_party_create_fail(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/')
    yield requests_mock.post(url=url, status_code=500, json={})


@pytest.fixture
def mock_party_get(requests_mock, data_standard_case):
    consignee = data_standard_case["case"]["data"]["consignee"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/{consignee["id"]}/')
    yield requests_mock.get(url=url, json={"data": consignee})


@pytest.fixture
def mock_party_put(requests_mock, data_standard_case):
    consignee = data_standard_case["case"]["data"]["consignee"]
    url = client._build_absolute_uri(f'/applications/{data_standard_case["case"]["id"]}/parties/{consignee["id"]}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture
def set_consignee_url(application_pk):
    return reverse("applications:set_consignee", kwargs={"pk": application_pk})


@pytest.fixture
def add_consignee_url(application_pk):
    return reverse("applications:add_consignee", kwargs={"pk": application_pk})


@pytest.fixture
def application_parties_consignee_summary_url(application_pk):
    return reverse("applications:consignee", kwargs={"pk": application_pk})


@pytest.fixture(autouse=True)
def setup(
    mock_countries,
    mock_get_application,
    mock_party_create,
    mock_party_get,
    mock_party_put,
):
    yield


@pytest.mark.parametrize("reuse_party_response, expected_url", ((True, "consignees_copy"), (False, "set_consignee")))
def test_add_consignee_view(
    application_pk, data_standard_case, add_consignee_url, authorized_client, reuse_party_response, expected_url
):
    response = authorized_client.get(add_consignee_url)

    assert response.status_code == 200
    assert response.context["form_title"] == "Do you want to reuse an existing party?"

    response = authorized_client.post(
        add_consignee_url,
        data={
            "reuse_party": reuse_party_response,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(f"applications:{expected_url}", kwargs={"pk": application_pk})


def test_set_consignee_view(set_consignee_url, authorized_client, requests_mock, data_standard_case, application_pk):
    party_id = data_standard_case["case"]["data"]["consignee"]["id"]
    response = test_set_consignee_steps(set_consignee_url, authorized_client)

    assert response.status_code == 302
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


def test_set_consignee_view_fail(
    set_consignee_url,
    authorized_client,
    requests_mock,
    data_standard_case,
    application_pk,
    mock_party_create_fail,
    caplog,
):
    response = test_set_consignee_steps(set_consignee_url, authorized_client)

    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.message == "Error creating party - response was: 500 - {}"

    soup = BeautifulSoup(response.content, "html.parser")
    error_message = soup.find("p", class_="govuk-body").get_text().strip()
    assert "Unexpected error creating party" == error_message


def test_set_consignee_steps(set_consignee_url, authorized_client):
    current_step_key = "set_consignee-current_step"
    response = authorized_client.get(set_consignee_url)

    assert response.context["form"].title == "Select the type of consignee"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_SUB_TYPE,
            f"{SetPartyFormSteps.PARTY_SUB_TYPE}-sub_type": "government",
        },
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee name"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_NAME,
            f"{SetPartyFormSteps.PARTY_NAME}-name": "test-name",
        },
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee website address (optional)"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_WEBSITE,
            f"{SetPartyFormSteps.PARTY_WEBSITE}-website": "https://www.example.com",
        },
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee address"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_ADDRESS,
            f"{SetPartyFormSteps.PARTY_ADDRESS}-address": "1 somewhere",
            f"{SetPartyFormSteps.PARTY_ADDRESS}-country": "US",
        },
    )

    return response


def test_set_consignee_website_validator(set_consignee_url, authorized_client):
    current_step_key = "set_consignee-current_step"
    response = authorized_client.get(set_consignee_url)

    assert response.context["form"].title == "Select the type of consignee"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_SUB_TYPE,
            f"{SetPartyFormSteps.PARTY_SUB_TYPE}-sub_type": "government",
        },
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee name"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_NAME,
            f"{SetPartyFormSteps.PARTY_NAME}-name": "test-name",
        },
    )
    assert not response.context["form"].errors
    assert response.context["form"].Layout.TITLE == "Consignee website address (optional)"

    response = authorized_client.post(
        set_consignee_url,
        data={
            f"{current_step_key}": SetPartyFormSteps.PARTY_WEBSITE,
            f"{SetPartyFormSteps.PARTY_WEBSITE}-website": "https://www.example.com/asfhadjksfhadsklfhalskfhjsakfhsdfkshfskfhsdkfhskfjhfkdshfksfhdksfhsdkjfhksfhsakadfshdsmnfbdsfbdsfsbdfdmsbfdfsngdfsbgdfsgdfsbgdfsgbdfsgbdfsgmnbdfsgmnbdfsgmdfsbgdfsgbdfsgbdfsbgdfsbg/",
        },
    )

    assert response.context["form"].errors.get("website")[0] == "Website address should be 200 characters or less"


def test_application_parties_consignee_summary(authorized_client, application_parties_consignee_summary_url):
    response = authorized_client.get(application_parties_consignee_summary_url)
    assertTemplateUsed(response, "applications/consignee.html")
